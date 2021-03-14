# botternaught

## Prerequisites
- Clone and cd into this repository
- Run MongoDB on `localhost:27017`
- Install requirements:
```sh
$ pip install -r requirements.txt
```

## Usage

### Data Aggregation
```sh
$ cd data
```
- Get Reddit authentication info [here](https://www.reddit.com/prefs/apps)
  - Click "create another app..."
    - name: botternaught
    - script
    - redirect uri: http://localhost:8080
  - Click create app
- Fill in the information inside the `praw.ini` inside this repository
![praw information](https://miro.medium.com/max/875/1*khszOCCaCtqZ6jM19uhpiQ.png)
- Run data aggregation
``` sh
$ python data_aggregation.py
```
