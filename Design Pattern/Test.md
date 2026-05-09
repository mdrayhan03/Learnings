# Biomass Regression: Improvement Action Plan

This plan outlines the steps to resolve the $R^2$ stagnation and interpretability issues (random LIME patterns) in your weight prediction model.

---

## 1. Structural Changes (The "Spatial" Fix) (Done)
Currently, your model uses `pooling='avg'`, which flattens all spatial data. The model loses the distinction between a "clover leaf" and "green-colored soil."

* **Remove Global Average Pooling:** Change the base model output to keep the 2D feature map.
* **Implement Spatial Attention:** Add a convolutional block that learns a weight for every pixel/region. This acts as a "soft" density map.
* **Why:** This forces the model to justify its weight prediction based on specific plant locations rather than an image-wide color average.

---

## 2. Refined Loss Strategy (Done)
Since you are predicting absolute grams (log-transformed), you need a loss that is robust to outliers but precise for small values.

* **Primary Loss:** **Log-Cosh Loss**. 
    * *Formula:* $L(y, \hat{y}) = \sum \log(\cosh(\hat{y} - y))$
    * *Rationale:* It provides smoother gradients than MAE and is less sensitive to the "heavy" high-biomass samples that often cause the spikes seen in your current RMSE curves.
* **Secondary Metric:** Keep monitoring **MAE**, but focus on **R2 Score** across different weight ranges (e.g., how does it perform on <5g vs >20g?).

---

## 3. Augmentation & Noise Tuning (Done)
Your current noise level is likely destroying the very textures (leaf edges) the model needs.

* **Reduce Gaussian Noise:** Lower the factor from `0.3` to `0.05`. High noise makes the image look like "static," forcing the model to rely on global color rather than leaf shape.
* **Add CoarseDropout (Cutout):** Instead of pixel noise, drop out square "chunks" of the image. This teaches the model to estimate total weight even when some plants are obscured or partially visible.
* **Color Constancy:** Keep the Hue/Saturation shifts but narrow the range. Clover and grass have very specific green signatures; shifting them too far might turn them into "dead" material in the model's eyes.

---

## 4. Training Schedule & Regularization
The gap between your training and validation loss indicates overfitting to the training textures.

* **Learning Rate Warmup:** Use a `CosineDecay` scheduler with a warmup phase. This prevents the model from "shattering" the pre-trained ImageNet weights in the first few epochs.
* **L2 Regularization (Weight Decay):** Increase the `weight_decay` in your `AdamW` optimizer to penalize overly complex weights.
* **Unfreeze Layers Gradually:** Instead of unfreezing `N` layers immediately, train the head first, then slowly unfreeze the ConvNeXt blocks from top to bottom.

---

## 5. Summary Checklist

| Category | Action | Priority |
| :--- | :--- | :--- |
| **Architecture** | Replace `pooling='avg'` with Spatial Attention block | **High** |
| **Loss Function** | Switch from Composite MAE/RMSE to **Log-Cosh** | **High** |
| **Augmentation** | Reduce Gaussian Noise to **0.05**; add **CoarseDropout** | **Medium** |
| **Optimizer** | Implement **Learning Rate Warmup** | **Medium** |
| **Evaluation** | Use **Saliency Maps** (Grad-CAM) to verify spatial focus | **Low** |

---

## Implementation Template (Attention Head)

```python
# Modified Head for build_model()
base_model = tf.keras.applications.ConvNeXtTiny(include_top=False, ...)
spatial_features = base_model.output # Shape: (Batch, H, W, C)

# Learn where the biomass is
attention_map = layers.Conv2D(1, (1, 1), activation='sigmoid')(spatial_features)
weighted_features = layers.Multiply()([spatial_features, attention_map])

# Global sum/average of the "attended" features
x = layers.GlobalAveragePooling2D()(weighted_features)
x = layers.Dense(128, activation='silu')(x)
outputs = layers.Dense(3, activation='linear')(x)