# Roo Code AI Model Training and Testing Framework

## Project Overview

This project provides a comprehensive framework for testing, fine-tuning, and training AI models, with a focus on improving interaction protocols for automated tooling such as **Roo Code**. The framework allows users to:
- Test and evaluate models.
- Fine-tune models based on specific interaction protocols.
- Perform efficient, low-token consumption communication for model training.
- Generate reproducible, high-quality model training results with a focus on integration and feedback.

## Key Features

- **Automated Test Generation**: Generate test cases for evaluating the performance of models in specific environments.
- **Reinforcement Learning**: Implement reinforcement learning techniques to fine-tune models based on feedback during testing and training.
- **Low-Token Communication**: Focus on minimizing token consumption while ensuring adherence to communication protocols.
- **Model Checkpoints**: Support for saving model states during training, enabling seamless continuation and evaluation at any point.
- **Gradio Interface**: An easy-to-use web interface for managing model testing and training.

## Folder Structure

The project follows a modular structure for easy integration and development.

- **/src/**: Contains all source code for the framework. Key components include:
  - `test_generator.py`: Generates test cases for model evaluation.
  - `test_runner.py`: Executes the generated tests on the model.
  - `evaluator.py`: Evaluates model performance based on test results.
  - `trainer.py`: Contains logic for model training, fine-tuning, and checkpoint management.
  - `model_manager.py`: Handles loading, managing, and interacting with models.
  - `docker_utils.py`: Utilities for Dockerized environments.
  
- **/configs/**: Configuration files for model and training setup, including hyperparameters.
  - `model_config.yaml`: Model configuration settings.
  - `training_config.yaml`: Hyperparameters and training settings.

- **/data/**: Stores test data, training data, and model checkpoints.
  - `test_data/`: Input data for generating test cases.
  - `training_data/`: Data used during model training.
  - `checkpoints/`: Saved model states during training.

- **/logs/**: Directory to store logs generated during training and evaluation.
  - `training_logs/`: Logs from model training sessions.

- **/notebooks/**: Example Jupyter notebooks for exploring the framework and generating test cases.

## Getting Started

Follow these steps to get the project up and running:

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/olilanz/Roo-Code-Model-Retrainer.git
cd Roo-Code-Model-Retrainer
```

### 2. Set Up Docker (Optional)

If you prefer to work in a Dockerized environment, make sure you have Docker installed and the following Dockerfile in place:

```bash
docker build -t model-training-framework .
```

### 3. Install Dependencies

Make sure you have Python 3.8+ and the required dependencies installed. You can install them via `pip`:

```bash
pip install -r requirements.txt
```

This will install the necessary libraries for model training, testing, and evaluation.

### 4. Configure Your Model

Edit the `configs/model_config.yaml` to specify the model you want to work with (e.g., `llama.cpp` or any other supported model). You can also adjust the `training_config.yaml` for hyperparameters.

### 5. Run Tests

To test the model's behavior using automatically generated test cases, run:

```bash
python src/test_runner.py --config configs/test_config.yaml
```

This will execute the tests on the selected model and provide feedback on its performance.

### 6. Train the Model

To start training the model, run the following command:

```bash
python src/trainer.py --config configs/training_config.yaml
```

You can monitor the progress and adjust training settings as needed.

### 7. Evaluate Performance

To evaluate the model's performance, run:

```bash
python src/evaluator.py --test-case /path/to/test_case.json
```

This will evaluate how well the model adheres to the desired interaction protocol.

### 8. Generate LoRa Files or Full Models

Once training is complete and you are satisfied with the performance, you can generate the LoRa file or a full model:

```bash
python src/model_manager.py --generate-lora
```

Alternatively, to merge training changes into a full model, use:

```bash
python src/model_manager.py --merge-model
```

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the open-source community for the development of libraries like `llama.cpp`, `Gradio`, and `PyTorch`, which have played an essential role in building this framework.

## Future Enhancements

- Support for distributed training across multiple machines.
- Integration with cloud platforms for scalable model training.
- Advanced hyperparameter tuning tools.
- Federated learning support.

For more information, check out the [documentation](./docs/) and [future roadmap](09-FUTURE.md).

---

Feel free to explore, contribute, and improve the framework as it evolves. If you have any questions or suggestions, don’t hesitate to reach out!
