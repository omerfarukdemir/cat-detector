YOLO based cat detector runs in Apple M1 chipset (not tested in any other processor architectures)

#### Requirements
- ```anaconda```/```miniconda```
#### Create environment
- ```conda env create -f m1.yaml```
#### Use environment
- ```conda activate cat-detector```
#### Update environment
- ```conda env update -f m1.yaml --prune```
#### Exit environment
- ```conda deactivate```
#### Remove environment
- ```conda env remove -n cat-detector```
#### Run
- Test file: ```python test.py```
- Application: ```flask run```
#### Results
<img src="./image/result.1.jpg" width="%100" />
<img src="./image/result.2.jpg" width="%100" />
<img src="./image/result.3.jpg" width="%100" />
<img src="./image/result.4.jpg" width="%100" />
