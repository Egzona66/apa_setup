
import numpy as np

import gym
from gym import spaces
from dm_env import specs
from dm_control import composer
from dm_control.locomotion.walkers import rodent

from modelling.corridor import Forceplate
from modelling.task import RunThroughCorridor
from modelling.utils import grab_frames, setup_video

_CONTROL_TIMESTEP = .02
_PHYSICS_TIMESTEP = 0.001



def build_environment(random_state=None):
    """Requires a rodent to run down a corridor with gaps."""

    # Build a position-controlled rodent walker.
    walker = rodent.Rat(
        observable_options={'egocentric_camera': dict(enabled=False)})

    # build forceplate arena
    arena = Forceplate()

    # Build a task that rewards the agent for running down the corridor at a
    # specific velocity.
    task = RunThroughCorridor(
        walker=walker,
        arena=arena,
        walker_spawn_position=(.2, 0, 0),
        walker_spawn_rotation=0,
        contact_termination=False,
        terminate_at_height=-0.3,
        physics_timestep=_PHYSICS_TIMESTEP,
        control_timestep=_CONTROL_TIMESTEP)

    return composer.Environment(time_limit=5,
                                task=task,
                                random_state=random_state,
                                strip_singleton_obs_buffer_dim=True)







class RLEnvironment(gym.Env):


    '''Turns a Control Suite environment into a Gym environment.
    
        mix of: https://github.com/fabiopardo/tonic/blob/0e20c894ee/tonic/environments/builders.py
        and: https://github.com/zuoxingdong/dm2gym/blob/master/dm2gym/envs/dm_suite_env.py
    '''

    def __init__(self,):
        self.env = build_environment()

        self.observation_space = convert_dm_control_to_gym_space(self.env.observation_spec())
        self.OBS_NAMES = list(self.observation_space.keys())
        self.action_space = convert_dm_control_to_gym_space(self.env.action_spec(), settype=np.int32)


    def seed(self, seed):
        self.env.task._random = np.random.RandomState(seed)

 
    def step(self, action):
        timestep = self.env.step(action)
        observation = {k:v for k, v in timestep.observation.items() if k in self.OBS_NAMES}
        reward = timestep.reward
        done = timestep.last()
        info = {}
        return observation, reward, done, info
    
    def reset(self):
        timestep = self.env.reset()
        return {k:v for k, v in timestep.observation.items() if k in self.OBS_NAMES}

    def render(self, mode='rgb_array', height=None, width=None, camera_id=0):
        '''Returns RGB frames from a camera.'''
        assert mode == 'rgb_array'
        return self.env.physics.render(
            height=height, width=width, camera_id=camera_id)



def convert_dm_control_to_gym_space(dm_control_space, settype=None):
    r"""Convert dm_control space to gym space. """
    if isinstance(dm_control_space, specs.BoundedArray):
        space = spaces.Box(low=dm_control_space.minimum, 
                           high=dm_control_space.maximum, 
                           dtype=settype or dm_control_space.dtype)
        assert space.shape == dm_control_space.shape
        return space
    elif isinstance(dm_control_space, specs.Array) and not isinstance(dm_control_space, specs.BoundedArray):
        if dm_control_space.shape == 0 or len(dm_control_space.shape) == 0 or dm_control_space.shape[0] == 0:
            return None
        space = spaces.Box(low=-float('inf'), 
                           high=float('inf'), 
                           shape=dm_control_space.shape, 
                           dtype=settype or dm_control_space.dtype)
        return space
    elif isinstance(dm_control_space, dict):
        vals = [convert_dm_control_to_gym_space(v, settype=settype) for v in dm_control_space.values()]
        space = spaces.Dict({k: v for k,v in zip(dm_control_space.keys(), vals) if v is not None})
        return space