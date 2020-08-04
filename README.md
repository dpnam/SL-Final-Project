# SL-Final-Project
Detect license plate motorbike in VN

# Cấu trúc thư mục
* colab: chứa tệp Python Notebook dùng để train trên Google Colab.
* raw-data: chứa dữ liệu gốc.
* data: chưa dữ liệu dùng để train và test.
* scripts: chứa các file scripts hỗ trợ chuẩn bị dữ liệu, ...
* src: chứa mã nguồn của website.

# Chạy website

* Cài đặt flask:
```sh
pip install flask
```

* Clone mã nguồn:
```sh
git clone https://github.com/dpnam/SL-Final-Project
cd SL-Final-Project/src
```

* Chạy trên linux:
```sh
export FLASK_ENV=development
export FLASK_APP=main.py
python -m flask run
```

* Chạy trên Windows: 
	* Command Prompt:
	```sh
	set FLASK_ENV=development
	set FLASK_APP=main.py
	python -m flask run
	```
	* PowerShell:
	```sh
	$env:FLASK_ENV = "development"
	$env:FLASK_APP = "main.py"
	python -m flask run
	```
