from ray.rllib.algorithms.ppo import PPOConfig
from snake import snake_env2
from ray.tune.logger import pretty_print
import ray

# ray.rllib.utils.check_env(snake_env.Snake()) 

config = PPOConfig()  
config = config.training(gamma=0.99, lr=0.01, kl_coeff=0.3, train_batch_size=10000, model={"fcnet_hiddens": [64, 64, 64, 64]})  
config = config.resources(num_gpus=0)  
config = config.rollouts(num_rollout_workers=4)  
config = config.evaluation(evaluation_num_workers=1)
# config = config.framework(framework='torch')
print(config.to_dict())  
# Build a Algorithm object from the config and run 1 training iteration.
algo = config.build(env="src.snake.snake_env.Snake")
# algo = config.build(env="CartPole-v1")

for _ in range(10):
    print(pretty_print(algo.train()))  # 3. train it,

print(pretty_print(algo.evaluate()))
# from ray.rllib.algorithms.ppo import PPOConfig


# algo = (
#     PPOConfig()
#     .rollouts(num_rollout_workers=1)
#     .resources(num_gpus=0)
#     .environment(env="CartPole-v1")
#     .build()
# )

# for i in range(10):
#     result = algo.train()
#     print(pretty_print(result))

#     if i % 5 == 0:
#         checkpoint_dir = algo.save()
#         print(f"Checkpoint saved in directory {checkpoint_dir}")
