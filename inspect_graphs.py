import tensorflow as tf


def load_graph(graph_file, use_xla=False):
    jit_level = 0
    config = tf.ConfigProto()
    if use_xla:
        jit_level = tf.OptimizerOptions.ON_1
        config.graph_options.optimizer_options.global_jit_level = jit_level

    with tf.Session(graph=tf.Graph(), config=config) as sess:
        gd = tf.GraphDef()
        with tf.gfile.Open(graph_file, 'rb') as f:
            data = f.read()
            gd.ParseFromString(data)
        tf.import_graph_def(gd, name='')
        ops = sess.graph.get_operations()
        n_ops = len(ops)
        return sess.graph, ops

sess, base_ops = load_graph('./model/graph.pb')
print(len(base_ops)) # 590
sess, frozen_ops = load_graph('./frozen/frozen_graph.pb')
print(len(frozen_ops)) # 45
sess, optimized_ops = load_graph('./frozen/optimized_graph.pb')
print(len(optimized_ops)) # 37
sess, quantized_ops = load_graph('./frozen/eightbit_graph.pb')
print(len(quantized_ops)) # 119
