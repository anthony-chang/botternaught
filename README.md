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
- Fill the information inside the `praw.ini` file inside this repository (replace the `placeholder`s)
![praw information](https://miro.medium.com/max/875/1*khszOCCaCtqZ6jM19uhpiQ.png)
- Run data aggregation
``` sh
$ python data_aggregation.py
```

### Clean Mongo Database
To reset the database (drop `redditors` collection from MongoDB):
```sh
$ cd data
$ python clean.py
```


## Known Issues
- Some data from Pushshift API seems to be broken
  - score (for both comments and submissions), num_comments, upvote_ratio, and probably some others are returning incorrect values
  - the data from PRAW API is correct, so we can switch to that if we need these attributes to be accurate
    - if we do this, we won't be able to easily alter the attributes in `attributes.py` so we should only do this after we confirm what attributes our model needs
