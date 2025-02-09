from modules.model import PatchEmbedding
import matplotlib.pyplot as plt
import torch
from torch import nn
from pathlib import Path


# Visualize a image
def plot_an_image(dataloader, class_names, patch_size):

    # 1. Get a batch of images
    image_batch, label_batch = next(iter(dataloader))

    # 2. Get a single image from the batch
    image, label = image_batch[0], label_batch[0]

    # 3. Shape of image tensor
    height, width = image.shape[1], image.shape[2]

    # 4. Get image tensor
    x = image.unsqueeze(0)

    # 5. Create patch embedding layer
    patch_embedding_layer = PatchEmbedding(in_channels=3,
                                           patch_size=patch_size,
                                           embedding_dim=768)

    # 6. Pass image through patch embedding layer
    patch_embedding = patch_embedding_layer(x)

    # 7. Create class token embedding
    batch_size = patch_embedding.shape[0]
    embedding_dimension = patch_embedding.shape[-1]
    class_token = nn.Parameter(torch.ones(
        batch_size, 1, embedding_dimension), requires_grad=True)

    # 8. Prepend class token embedding to patch embedding
    patch_embedding_class_token = torch.cat(
        (class_token, patch_embedding), dim=1)

    # 9. Create position embedding
    number_of_patches = int((height * width) / patch_size**2)
    position_embedding = nn.Parameter(torch.ones(
        1, number_of_patches+1, embedding_dimension), requires_grad=True)

    # 10. Add position embedding to patch embedding with class token
    patch_and_position_embedding = patch_embedding_class_token + position_embedding
    print(
        f"Patch + token + position embeddings: {patch_and_position_embedding.shape}")

    # 11. Plot image with matplotlib
    plt.imshow(image.permute(1, 2, 0))
    plt.title(class_names[label])
    plt.axis(False)


# Set seeds
def set_seeds(seed=42):
    """Sets random sets for torch operations.

    Args:
        seed (int, optional): Random seed to set. Defaults to 42.
    """
    # Set the seed for general torch operations
    torch.manual_seed(seed)
    # Set the seed for CUDA torch operations (ones that happen on the GPU)
    torch.cuda.manual_seed(seed)


def save_model(model, target_dir, model_name):
    # Create target directory
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True,
                          exist_ok=True)

    # Create model save path
    model_save_path = target_dir_path / model_name

    # Save the model state_dict()
    print(f"[INFO] Saving model to: {model_save_path}")
    torch.save(obj=model.state_dict(),
               f=model_save_path)
