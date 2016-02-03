###CUDA_PATH=/opt/local/cuda42
###SDK_PATH=/home/Tit2/berczik/NVIDIA_GPU_Computing_SDK/C

###CUDA_PATH=/opt/local/cuda50
###SDK_PATH=/opt/local/cuda50/samples

###CCC=/usr/lib64/openmpi/bin/mpiCC
###CCC=mpiCC.openmpi
###CCC=mpiCC
CCC=/usr/local/Cellar/open-mpi/1.10.1_1/bin/mpicc



CXXFLAGS = -O3
### -Wall -FPIC
### -fopenmp

gpu: gpu-4th gpu-6th gpu-8th

asm: gpu-4th.s gpu-6th.s gpu-8th.s

cubin: hermite4-gpu.cubin hermite6-gpu.cubin hermite8-gpu.cubin

cpu: cpu-4th cpu-6th cpu-8th

clean:
	rm -f *.o *.s *.cubin .*.swp


gpu-8th: phi-GPU.cpp hermite8-gpu.o
	$(CCC) $(CXXFLAGS) -DEIGHTH -DGPU -I$(CUDA_PATH)/include -L$(CUDA_PATH)/lib64  -o $@ $^ -lcudart

gpu-6th: phi-GPU.cpp hermite6-gpu.o
	$(CCC) $(CXXFLAGS) -DSIXTH -DGPU -I$(CUDA_PATH)/include -L$(CUDA_PATH)/lib64  -o $@ $^ -lcudart

gpu-4th: phi-GPU.cpp hermite4-gpu.o
	$(CCC) $(CXXFLAGS) -DFOURTH -DGPU -I$(CUDA_PATH)/include -L$(CUDA_PATH)/lib64 -lcudart -o $@ $^ -lcudart


gpu-8th.s: phi-GPU.cpp
	$(CCC) $(CXXFLAGS) -DEIGHTH -DGPU -I$(CUDA_PATH)/include  -S -o $@ $<

gpu-6th.s: phi-GPU.cpp
	$(CCC) $(CXXFLAGS) -DSIXTH -DGPU -I$(CUDA_PATH)/include  -S -o $@ $<

gpu-4th.s: phi-GPU.cpp
	$(CCC) $(CXXFLAGS) -DFOURTH -DGPU -I$(CUDA_PATH)/include  -S -o $@ $<


hermite8-gpu.o: hermite8-gpu.cu hermite8-gpu.h
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -c $<

hermite6-gpu.o: hermite6-gpu.cu hermite6-gpu.h
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -c $<

hermite4-gpu.o: hermite4-gpu.cu hermite4-gpu.h
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -c $<


hermite8-gpu.cubin: hermite8-gpu.cu
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -cubin $<

hermite6-gpu.cubin: hermite6-gpu.cu
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -cubin $<

hermite4-gpu.cubin: hermite4-gpu.cu
	nvcc -I $(SDK_PATH)/common/inc -Xcompiler "-O3 -FPIC" -cubin $<


cpu-8th: phi-GPU.cpp hermite8.h
	$(CCC) $(CXXFLAGS) -DEIGHTH -o $@ $<

cpu-6th: phi-GPU.cpp hermite6.h
	$(CCC) $(CXXFLAGS) -DSIXTH  -o $@ $<

cpu-4th: phi-GPU.cpp hermite4.h
	$(CCC) $(CXXFLAGS) -DFOURTH -o $@ $<

