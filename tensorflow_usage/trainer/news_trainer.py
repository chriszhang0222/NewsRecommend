import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics
from tensorflow_usage.trainer.cnn_model import generate_cnn_model
from common.utils.news_classes import classes
REMOVE_PREVIOUS_MODEL = True
learn = tf.contrib.learn

MODEL_OUTPUT_DIR = '../model/'
DATA_SET_FILE = '../data/test.csv'
VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'
MAX_DOCUMENT_LENGTH = 75
N_CLASSES = len(classes)

# Training parms
STEPS = 20


def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        print("Removing previous model...")
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE, header=None)
    df = df.sample(frac=1)
    train_df = df[:600]
    test_df = df.drop(train_df.index)

    # x - news description, y - class
    x_train = train_df[1]
    y_train = train_df[0]
    x_test = test_df[1]
    y_test = test_df[0]

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    print(('Total words: %d' % n_words))

    # Saving n_words and vocab_processor:
    with open(VARS_FILE, 'wb') as f:  # needs to be opened in binary mode.
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    classifier = learn.Estimator(
        model_fn=generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=STEPS)

    # Evaluate model
    # y_predicted = [
    #     p['class'] for p in classifier.predict(x_test, as_iterable=True)
    # ]

    text_series = pd.Series(["Watch: BLACKPINK Reveals Teaser For New Project “BLACKPINK – Around The World”"])
    predict_x = np.array(list(vocab_processor.transform(text_series)))

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]


    # score = metrics.accuracy_score(y_test, y_predicted)
    # print(('Accuracy: {0:f}'.format(score)))
    print('Classify:{}'.format(y_predicted[0]))

    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]
    score = metrics.accuracy_score(y_test, y_predicted)
    print(('Accuracy: {0:f}'.format(score)))




if __name__ == '__main__':
    tf.app.run(main=main)