# Task Knowledge

<!-- METADATA:SESSION=0 -->

## Working Rules
- Do not train; only evaluate the official pretrained BC-RNN checkpoint.
- Keep all downloaded checkpoints, rollout logs, videos, and reports under the intern_method_developer task directory.
- Treat robomimic / robosuite version differences as first-order experimental variables.

## Official References
- Model-zoo entry: `https://robomimic.github.io/docs/model_zoo/robomimic_v0.1.html`
- Official eval tutorial: `https://robomimic.github.io/docs/tutorials/using_pretrained_models.html`

## Findings
- Official target: Square(PH), low-dimensional BC-RNN, approximate success rate 84%.
- Official tutorial uses 50 rollouts, horizon 400, seed 0, and can save video with `--video_path`.
