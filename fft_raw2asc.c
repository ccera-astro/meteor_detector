// Take output of GNURadio Log Power FFT
// Convert raw 4-byte float data to numerical 
// Rearrange bins to show linearly increasing frequency in GNUPlot

// NOTE: This code makes an assumption about both float and gnuradio's format being a 4byte size
// so it's portability is very poor.

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>


int main(int argc, char *argv[]) {

  FILE *input_file, *output_file;
  int frame,bin,frame_size,fft_size;
  float pwr_val;
  float *raw_frame;
  struct stat st;
  float bw;

  if ( argc < 5 ) {
    printf("\nUsage: fft_raw2asc <input file> <output file> <vector_size> <bandwidth>\n");
    printf("Exampel: ./fft_raw2asc adc_data adc_num 1024 1000 \n");
    exit(1);
  }

  if ( (input_file = fopen(argv[1],"r")) == NULL ) {
    perror("Input file");
    exit(1);
  }

  if ( (output_file = fopen(argv[2],"w")) == NULL ) {
    perror("Output file");
    exit(1);
  }
  
  //fseek(input_file,atoi(argv[3]),SEEK_SET);
  //frame_size=atoi(argv[4]);
  fft_size=atoi(argv[3]);
  raw_frame=malloc(fft_size*4);
  
  bw = (float)atof(argv[4]);

  // Find size of file
  // fstat((int)input_file,&st);
  stat(argv[1],&st);
  frame_size=st.st_size/(fft_size * 4);
  
  printf("file size=%d, FFT Size=%d, Number of complete FFT Frames=%d\n",(int)st.st_size,fft_size,frame_size);

  
  for (frame=0;frame<frame_size;frame++) {
	  float startf;
    for (bin=0;bin<fft_size;bin++) {
      if (fread(&pwr_val,4,1,input_file) == 0) {
	if (feof(input_file))
	  printf("Input reached EOF\n");
	else
	  printf("Error with input file\n");
	break;
      }
      raw_frame[bin]=pwr_val;
    }
    
    startf = -(bw/2.0);
    for (bin=fft_size/2;bin<fft_size;bin++) {
		
      fprintf(output_file,"%f %f %f\n",startf, (float)frame*(fft_size/bw), raw_frame[bin]);
      startf += bw/(float)fft_size;
    }
    for (bin=0;bin<fft_size/2;bin++) {
      fprintf(output_file,"%f %f %f\n",startf, (float)frame*(fft_size/bw), raw_frame[bin]);
      startf += bw/(float)fft_size;
    }

    fprintf(output_file,"\n");
  }
  fclose(input_file);
  fclose(output_file);
}



