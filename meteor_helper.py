import sys
import time
import threading
import os
HZ=40
NUMCHANS=10
HISTSIZE=60*HZ
INITAVG=60*HZ
DAMPING=45*HZ

ST_AVERAGING=1
ST_LOOKING=2
ST_TRIGGERED=3
lock=threading.Lock()
sample_counter=[0]*NUMCHANS
sampling_started=[0.0]*NUMCHANS
sample_history=[[0.0]*HISTSIZE]*NUMCHANS
sample_histtods=[[0.0]*HISTSIZE]*NUMCHANS
sample_averages=[0]*NUMCHANS
sample_states=[ST_AVERAGING]*NUMCHANS
sample_avgcnt=[INITAVG]*NUMCHANS
hysteresis=[DAMPING]*NUMCHANS
event_counter=[0]*NUMCHANS
freqs=[0]*NUMCHANS
fps=[None]*NUMCHANS
filenames=[""]*NUMCHANS
last_threshold=[0]*NUMCHANS
last_time=[0]*NUMCHANS
rate_estimate=[0]*NUMCHANS
threads_started=0
baseband_threads=[None]*NUMCHANS
bb_record=[False]*NUMCHANS
gains=[1]*NUMCHANS
daily_counters=[0]*NUMCHANS
last_reavg=[0]*NUMCHANS

def write_chan(num,chdata,freq,thresh,rec,gain):
#
# Change in freq or threshold?  Reset to ST_AVERAGING
#     
    bb_record[num] = rec
    
    current_sample_time = time.time()
    sample_counter[num] = sample_counter[num] + 1
    
    if (sample_counter[num] % HZ) == 0:
        fn = makename(int(current_sample_time),num,"met-daily",-1)
        fp = open(fn, "a")
        record(fp,current_sample_time,chdata,freqs[num],sample_averages[num],num)
        fp.close()
    
    if freq != freqs[num] or thresh != last_threshold[num] or gain != gains[num]:
        last_threshold[num] = thresh
        gains[num] = gain
        sample_states[num] = ST_AVERAGING
        sample_avgcnt[num] = INITAVG
        sample_averages[num] = 0
        freqs[num] = freq
        if fps[num] != None:
            fps[num].close
            fps[num] = None

#
# Pull appropriate history record
#
    lock.acquire()
    l = sample_history[num]
    lt = sample_histtods[num]

#
# Shift history
#
    l = shift(sample_history[num],1)
    lt = shift(sample_histtods[num],1)
#
# Insert fresh data
#    
    l[len(l)-1] = chdata
    lt[len(l)-1] = current_sample_time
    
#
# Stuff shifted/updated record back into history
#
    sample_history[num] = l
    sample_histtods[num] = lt
    
    lock.release()
#
# In ST_AVERAGING?
# Compute average for INITAVG samples
#       
    if sample_states[num] == ST_AVERAGING:
        if sample_avgcnt[num] > 0:
            sample_averages[num] = sample_averages[num] + chdata
            sample_avgcnt[num] = sample_avgcnt[num] - 1
        else:
            sample_states[num] = ST_LOOKING
            sample_averages[num] = sample_averages[num] / INITAVG
            
        return "/dev/null"
        
#
# If current sample exceeds our threshold
#
    if chdata > (sample_averages[num]*thresh):
        
        hysteresis[num] = DAMPING
#
# If currently "looking" for a trigger start
# Update to "TRIGGERED", and dump the history
#  
        if sample_states[num] == ST_LOOKING:
            sample_states[num] = ST_TRIGGERED
            q = current_sample_time
            d = current_sample_time - last_time[num]
            r = 3600.0 / d
            rate_estimate[num] = 0.60*r + (0.40 * rate_estimate[num])
            last_time[num] = current_sample_time
            if filenames[num] != makename(q,num,"met-det",event_counter[num]) or fps[num] == None:
                if fps[num] != None:
                    fps[num].close
            fps[num]=open(makename(q,num,"met-det",event_counter[num]), "a")
            filenames[num] = makename(q,num,"met-det",event_counter[num])
            event_counter[num] = event_counter[num] + 1
            for i in range(0,len(l)):
                record(fps[num],lt[i],l[i],freq,sample_averages[num],num)

#
# Already TRIGGERED
# Dump current sample
#          
        elif sample_states[num] == ST_TRIGGERED and fps[num] != None:
            record(fps[num],current_sample_time,chdata,freq,sample_averages[num],num)
#
# We've been recording samples for 5.5 minutes already?  That's suspicious--
#   reset to ST_AVERAGING, because likely what has happened is that we've had a significant upwards
#   baseline shift
#
            if current_sample_time - last_time[num] > (5.5*60):
                sample_states[num] = ST_AVERAGING
                sample_avgcnt[num] = INITAVG
                sample_averages[num] = 0.0
                fps[num].close
                fps[num] = None
#
# Sample doesn't exceed threshold
#           
    else:
#
# If haven't adjusted baseline in a while and haven't been above thresh in a while
#
        if current_sample_time - last_reavg[num] > (7*60) and sample_states[num] == ST_LOOKING:
            l = sample_history[num]
            sample_averages[num] = sum(l)/len(l)
            last_reavg[num] = current_sample_time
#
# If currently TRIGGERED
#           
        if sample_states[num] == ST_TRIGGERED:
#
# Hysteresis timer expired?  Update to LOOKING again
#
            if hysteresis[num] <= 0:
                sample_states[num] = ST_LOOKING
                if fps[num] != None:
                    fps[num].close()
                    fps[num] = None
#
# Decrement hysteresis timer, and dump current sample
#
            else:
                hysteresis[num] = hysteresis[num] - 1
                record(fps[num],current_sample_time,chdata,freq,sample_averages[num],num)

    return "/dev/null"

def trig_state(num,val):
    est = "%.3f" % rate_estimate[num]
    if sample_states[num] == ST_TRIGGERED:
        return ["TRIGGERED",str(filenames[num]),str(event_counter[num]),str(est)]
    elif sample_states[num] == ST_LOOKING:
        return ["TRIG SEARCH","None",str(event_counter[num]),str(est)]
    elif sample_states[num] == ST_AVERAGING:
		return ["AVERAGING", "None", str(event_counter[num]),str(est)]
    else:
		return ["UNKNOWN", "None", str(event_counter[num]),str(est)]

def current_time(val):
    ltp = time.localtime()
    tod = "%02d:" % (ltp.tm_hour)
    tod = tod + "%02d:" % (ltp.tm_min)
    tod = tod + "%02d" % (ltp.tm_sec)
    return tod

def makename(tod,num,prefix,evct):
    if tod != 0:
        ltp = time.localtime(tod)
    else:
        ltp = time.localtime()
    nam = prefix
    nam = nam + "%d-" % num
    if evct != -1:  
        nam = nam+"%02d" % (ltp.tm_hour)
        nam = nam+"%02d-" % (ltp.tm_min)
        
    nam = nam + "%04d" % (ltp.tm_year)
    nam = nam + "%02d" % (ltp.tm_mon)
    nam = nam + "%02d" % (ltp.tm_mday)
    nam = nam + ".dat"
    return nam

def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

def record(fp,tod,chdata,freq,avg,num):
    if fp != None:
        frac = tod - int(tod)
        ltp = time.localtime(tod)
        hours = ltp.tm_hour
        hours = hours + float(ltp.tm_min/60.0)
        secs = float(ltp.tm_sec) + frac
        hours = hours + float(secs/3600.0)
        hstr = "%.6f" % hours
        wstr = hstr+' '+str(chdata)
        if sample_counter[num] % (HZ*5) == 0:
            wstr = wstr+' '+str(freq)
            wstr = wstr+' '+str(rate_estimate[num])
        fp.write(wstr+'\n')


def baseband_thread(fname,ndx):
    fp = None
    state = 0
    f = os.open(fname, os.O_RDONLY|os.O_NONBLOCK)
    while True:
        try:
            data = os.read(f,2048)
        except:
            time.sleep(0.05)
            continue
        if bb_record[ndx] != True:
            continue
        if len(data) > 0:
            st = sample_states[ndx]
            if st == ST_TRIGGERED:
                if state == 0:
                    if fp != None:
                        fp.close()
                    state = 1
                    fp = open(makename(0,ndx,"met-bb",event_counter[ndx]), "w")
                fp.write(data)
            else:
                if fp != None:
                    fp.close()
                    fp = None
                state = 0
        else:
            time.sleep(0.1)
                
def start_threads(files):
    global threads_started
    if threads_started == 0:
        threads_started = 1
        for i in range(0,len(files)):
            baseband_threads[i] = threading.Thread(target=baseband_thread,args=[files[i],i+1])
            baseband_threads[i].daemon = True
            baseband_threads[i].start()
    return len(files)

def getHz():
    return HZ


def fmt(val):
    x = "%.4f" % (val/1.0e6)
    x = x + "M"
    return x

def text_float_formatter(val):
    return "%.4e" % val     
