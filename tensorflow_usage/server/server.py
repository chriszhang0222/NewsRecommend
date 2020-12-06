import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import logging
import time
from common.utils.news_classes import *

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from common.utils.news_classes import classes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tensorflow_usage.trainer.cnn_model import generate_cnn_model
logging.basicConfig(level=logging.INFO,  format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
Logger = logging.getLogger(__name__)

learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = len(classes)

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

n_words = 200

MAX_DOCUMENT_LENGTH = 500
vocab_processor = None
classifier = None


def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE
    )


def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR
    )

    df = pd.read_csv('../data/test.csv', header=None)
    df = df.sample(frac=1)
    train_df = df
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)
    Logger.info('Model Update')


restoreVars()
loadModel()


class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        Logger.info('Model update detected. Loading new model.')
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        restoreVars()
        loadModel()


observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()


def classify(text):
    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    Logger.info(predict_x)

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    Logger.info((y_predicted[0]))
    topic = class_map[str(y_predicted[0])]
    Logger.info(text)
    return topic
# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')

print(("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT)))

RPC_SERVER.serve_forever()