import numpy as np
import tensorflow as tf
import os
import random
from dataloader import GenDataLoader, DisDataLoader, DataProcessing, PrefixLoader
from classifier import RFCBased, EntropyClustering, IPv62Vec
import pickle
from generator import Generator
from discriminator import Discriminator
# from rollout import ROLLOUT

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
gpu_options = tf.GPUOptions(allow_growth=True)
# gpu_options = tf.compat.v1.GPUOptions(allow_growth=True)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
# sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))

#########################################################################################
#  Generator  Hyper-parameters
#########################################################################################
EMB_DIM = 200  # embedding dimension 200
HIDDEN_DIM = 200  # hidden state dimension of lstm cell 200
MAX_SEQ_LENGTH = 33  # max sequence length
BATCH_SIZE = 64


#########################################################################################
#  Discriminator  Hyper-parameters
#########################################################################################
dis_embedding_dim = 64
dis_filter_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
dis_num_filters = [100, 200, 200, 200, 200, 100, 100, 100, 100, 100, 160]
dis_dropout_keep_prob = 0.75
dis_l2_reg_lambda = 0.2
dis_batch_size = 64


#########################################################################################
#  Basic Training Parameters
#########################################################################################
TOTAL_EPOCH = 5
# # 46400 464000 2320000 4640000
# # 44900 449000 2245000 4490000
# TOTAL_GENERATION = 46400//5
CLASSIFICATION_METHOD = 0  # 0-rfc, 1-ec, 2-ipv62vec, -1-none
ALIAS_DETECTION = 0

out = "dataset3_little_copy/"

dataset_path = out+"source_data/"
save_path = out+"save_data/"
# candidate_path = out+"candidate_set_{}/".format(TOTAL_GENERATION)
model_path = out+"models/"
category_path = out+'category_data/'

os.makedirs(os.path.dirname(save_path),exist_ok=True)
# os.makedirs(os.path.dirname(candidate_path),exist_ok=True)
os.makedirs(os.path.dirname(model_path),exist_ok=True)
# in
source_file = dataset_path + "responsive-addresses.txt"
aliased_prefix_file = dataset_path + "aliased-prefixes.txt"

# out
work_file = dataset_path + "responsive-addresses.work"
emb_data_file = dataset_path + "responsive-addresses.data"
emb_dict_file = dataset_path + "responsive-addresses.vocab"
emb_id_file = dataset_path + "responsive-addresses.id"



# out
log_file = save_path + "train.log"
eval_file = save_path + "eval_file.txt"
eval_text_file = save_path + "eval_text_file.txt"

rfc_profile = save_path+'rfc_profile.txt'
ec_profile = save_path+'ec_profile.txt'
ec_cluster = save_path+'ec_cluster.txt'
ipv62vec_profile = save_path+'ipv62vec_profile.txt'

rfc_data_path = category_path + 'rfc/data/'
rfc_id_path = category_path + 'rfc/id/'
ec_id_path = category_path + 'ec/id/'
ec_data_path = category_path + 'ec/data/'
ipv62vec_data_path = category_path + 'ipv62vec/data/'
ipv62vec_id_path = category_path + 'ipv62vec/id/'


def generate_infer(sess, trainable_model, epoch, vocab_list, generator_id,total_generation,candidate_path):
    generated_samples = []
    for _ in range(int(total_generation / BATCH_SIZE)):
        generated_samples.extend(trainable_model.generate(sess))
    file = candidate_path + 'candidate_generator_' + str(generator_id) + '_epoch_' + str(epoch) + '.txt'
    target_generation = []
    for address in generated_samples:
        address = list(address)
        if 1 in address:
            address = address[:address.index(1)]
        count = 0
        predict_address_str = ""
        for i in address[:-1]:
            predict_address_str += vocab_list[i]
            count += 1
            if count % 4 == 0 and count != 32:
                predict_address_str += ":"
        target_generation.append(predict_address_str + '\n')
    fout = open(file, 'w')
    fout.writelines(list(set(target_generation)))
    fout.close()
    print("%s saves" % file)
    return




def load_emb_data(emb_dict_file):
    word_dict = {}
    word_list = []
    item = 0
    with open(emb_dict_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            word = line.strip()
            word_dict[word] = item
            item += 1
            word_list.append(word)
    length = len(word_dict)
    print("Load embedding success! Num: %d" % length)
    return word_dict, length, word_list











def main():
    budgets = [5000]
    # budgets = [46400,464000,2320000,4640000]
    # 44900 449000 2245000 4490000
    # budgets = [44900,449000,2245000,4490000]
    # load embedding info
    vocab_dict, vocab_size, vocab_list = load_emb_data(emb_dict_file)
    generator_num = 6
    generators = np.array([Generator(vocab_size, vocab_dict, BATCH_SIZE, EMB_DIM, HIDDEN_DIM, MAX_SEQ_LENGTH, i)
                        for i in range(generator_num)])
    for budget in budgets:
        total_genaration = budget
        candidate_path = out+"candidate_set_{}/data/".format(budget)
        os.makedirs(os.path.dirname(candidate_path),exist_ok=True)
        for total_batch in range(1, TOTAL_EPOCH + 1):
        # Test
            if total_batch % 5 == 0:
                for i in range(generator_num):
                    print('Generator %s/%s' % (i + 1, generator_num))
                    generators[i].load_model(sess, model_path, str(i + 1))
                    generate_infer(sess, generators[i], total_batch, vocab_list, i + 1,total_genaration,candidate_path)
                    # generators[i].save_model(sess, model_path, str(i + 1))

    

if __name__ == '__main__':
    main()


