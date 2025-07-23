from typing import Dict, Type

import numpy as np
import tensorflow as tf
# import tensorflow.keras.backend as K
import ray
from ray.rllib.models import ModelCatalog
from ray.rllib.utils.annotations import override
from ray.rllib.models.misc import linear, normc_initializer


def __tmp5(__tmp7: <FILL>, __tmp3, networks):
    """
    Constructs a Ray policy with multiple models as part of the collections. This
    allows for distributed training with multiple parameter sets (for example, 
    when using auxillary losses)
    
    Arguments:
        policy_model {Type[tf.keras.Model]} -- The policy model which is called to make predictions
        networks {Dict[str, tf.keras.Model]} -- A dictionary of additional networks
    
    Returns:
        ray.rllib.models.Model -- A model which can be used with Ray
    """

    class __typ0(ray.rllib.models.Model):

        @override(ray.rllib.models.Model)
        def __tmp4(__tmp0, __tmp6, __tmp2, options):

            # Setup the policy model
            if tf.get_collection('_rk_policy_model'):
                __tmp0.model = tf.get_collection('_rk_policy_model')[0]
            else:
                __tmp0.model = __tmp3(__tmp2, **options)
                tf.add_to_collection('_rk_policy_model', __tmp0.model)

            # Add any other models to the collection
            if networks:
                __tmp0.networks = {}
            for key in networks.keys():
                if tf.get_collection('_rk_networks_{}'.format(key)):
                    __tmp0.networks[key] = tf.get_collection('_rk_networks_{}'.format(key))
                else:
                    __tmp0.networks[key] = [networks[key](**options), None, None]
                    tf.add_to_collection('_rk_networks_{}'.format(key), __tmp0.networks[key])

            if __tmp0.model.recurrent:
                __tmp0.state_init = [
                    np.zeros([state_size]) for state_size in __tmp0.model.state_size]

                if not __tmp0.state_in:
                    __tmp0.state_in = [tf.placeholder(tf.float32, [None, state_size])
                                     for state_size in __tmp0.model.state_size]

                output = __tmp0.model(__tmp6,
                                    seqlens=__tmp0.seq_lens,
                                    initial_state=__tmp0.state_in)
                __tmp0.state_out = list(output['state_out'])
            else:
                output = __tmp0.model(__tmp6)
            __tmp0.policy_output = output

            # Update the input dict with the model outputs
            __tmp6['model_outputs'] = output

            # Compute the outputs for each of the networks
            for key, net in __tmp0.networks.items():
                if net[0].recurrent:
                    net[1] = [
                        np.zeros([state_size]) for state_size in net[0].state_size]

                    if not net[2]:
                        net[2] = [tf.placeholder(tf.float32, [None, state_size])
                                        for state_size in net[0].state_size]

                    __tmp0.network_outputs[key] = net[0](__tmp6,
                                                        seqlens=__tmp0.seq_lens,
                                                        initial_state=net[2])
                else:
                    __tmp0.network_outputs[key] = net[0](__tmp6)

            return output['logits'], output['latent']

        @override(ray.rllib.models.Model)
        def custom_loss(__tmp0, __tmp1, loss_inputs):


            # Update the loss_inputs with all of the model outputs
            if __tmp0.networks:
                loss_inputs['network_outputs'] = {k:__tmp0.network_outputs[k] for k in __tmp0.networks.keys()}
                loss_inputs['network_outputs']['policy_model'] = __tmp0.policy_output

            total_loss = __tmp1
            if hasattr(__tmp0.model, 'custom_loss'):
                total_loss = __tmp0.model.custom_loss(__tmp1, loss_inputs)

            if __tmp0.networks:
                for _, net in __tmp0.networks.items():
                    if hasattr(net[0], 'custom_loss'):
                        total_loss = net[0].custom_loss(total_loss, loss_inputs, )
                return total_loss

    __typ0.__name__ = __tmp7
    __typ0.__doc__ = "Wraped Multi-Network RAY policy"

    ModelCatalog.register_custom_model(__tmp7, __typ0)

    return __typ0
