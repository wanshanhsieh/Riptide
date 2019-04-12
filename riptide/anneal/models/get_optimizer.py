import tensorflow as tf

_NUM_IMAGES = 1281167


def adam_piecewise(global_step, batch_size, num_gpus):
    if num_gpus == 0:
        num_gpus = 1

    batch_size = batch_size * num_gpus

    starting_lr = 1e-4

    # Adjust starting lr for batch size.
    batch_denom = 128.
    lr_adjustment = batch_size / batch_denom
    starting_lr = starting_lr * lr_adjustment

    lr_decay = 0.2
    lr_values = [
        starting_lr, starting_lr * lr_decay, starting_lr * lr_decay * lr_decay
    ]
    epoch_boundaries = [56, 64]
    steps_per_epoch = _NUM_IMAGES / batch_size
    step_boundaries = [int(x * steps_per_epoch) for x in epoch_boundaries]
    lr_schedule = tf.compat.v1.train.piecewise_constant_decay(
        global_step, boundaries=step_boundaries, values=lr_values)
    optimizer = tf.compat.v1.train.AdamOptimizer(
        learning_rate=lr_schedule, epsilon=1e-5)
    return optimizer, lr_schedule


def get_optimizer(name, global_step, batch_size, num_gpus=1):
    models = {
        'alexnet': adam_piecewise,
    }

    return models[name](global_step, batch_size, num_gpus)
