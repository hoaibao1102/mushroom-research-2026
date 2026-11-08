# Target system requirements extracted from the project brief

## Operating scene

- Camera view is horizontal/side-on.
- Mushrooms emerge from multiple positions on cultivation columns or containers.
- The same physical view should be captured repeatedly, initially once per day.
- Multiple columns/trays/batches may need comparison.

## Required capabilities

### Recognition

Detect mushrooms as a general target rather than restricting the first model to one species. Distinguish mushrooms from non-mushroom objects in real cultivation scenes. Use instance segmentation when boundary quality is needed for measurement.

### Temporal tracking and measurement

Associate clusters already observed on prior days with new detections. Track visible clusters as groups rather than requiring each fruitbody to have a permanent ID. Measure changes in size, count and developmental state over time.

### Cultivation evaluation

Store results by column or grow unit and by production batch. Enable comparisons of growth rates and outcomes under different cultivation conditions. Join temperature, humidity and other environment data where timestamps and unit identity are available.

### Model updates

Retain daily images and the model's predictions. Select useful or uncertain examples for human review. Update models in batches without restarting from scratch whenever possible. Check each candidate update against old/reviewed data before deployment to avoid regressions.

## Preferred delivery split

- Train and validate models on Google Colab GPU.
- Export model weights/configuration to local storage.
- Run inference, tracking, measurements, database and dashboard locally.
- Prioritize AMD GPU acceleration on the RX 5500 XT, while keeping CPU inference as a dependable fallback.
