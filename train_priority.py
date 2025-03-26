try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader
    import numpy as np
except ModuleNotFoundError as e:
    print("Torch is not installed. Please install it using 'pip install torch'.")
    raise e

# Define a dataset class
class TaskDataset(Dataset):
    def __init__(self, task_data, order_labels):
        self.task_data = torch.tensor(task_data, dtype=torch.float32)
        self.order_labels = torch.tensor(order_labels, dtype=torch.long)
    
    def __len__(self):
        return len(self.task_data)
    
    def __getitem__(self, idx):
        return self.task_data[idx], self.order_labels[idx]

# Define an MLP model
class MLP(nn.Module):
    def __init__(self, input_size, output_size, hidden_size=128):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)  # Output is raw scores for ordering
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Sample data format (n tasks, each with (T, C))
# Assume each task set has n=5 tasks
sample_task_data = [
    [10, 3, 20, 5, 15, 4, 25, 6, 30, 7],  # Task set 1 (flattened (T,C) pairs)
    [12, 4, 22, 6, 18, 5, 28, 7, 35, 8]   # Task set 2
]
sample_order_labels = [
    [1, 3, 2, 5, 4],  # Optimal priority order for task set 1
    [2, 4, 1, 5, 3]   # Optimal priority order for task set 2
]

# Convert to numpy arrays
sample_task_data = np.array(sample_task_data)
sample_order_labels = np.array(sample_order_labels) - 1  # Convert to 0-based indexing

# Hyperparameters
input_size = sample_task_data.shape[1]  # 2 * n tasks (flattened T, C pairs)
output_size = sample_order_labels.shape[1]  # Number of tasks (n)
hidden_size = 128
batch_size = 16
epochs = 100
learning_rate = 0.001

# Create dataset and dataloader
dataset = TaskDataset(sample_task_data, sample_order_labels)
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize model, loss function, and optimizer
model = MLP(input_size, output_size, hidden_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(epochs):
    total_loss = 0
    for task_batch, order_batch in dataloader:
        optimizer.zero_grad()
        outputs = model(task_batch)
        loss = criterion(outputs, order_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    if (epoch + 1) % 10 == 0:
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")

# Example inference
with torch.no_grad():
    test_task = torch.tensor([[14, 4, 24, 5, 16, 6, 26, 7, 32, 8]], dtype=torch.float32)
    pred_order = model(test_task).argmax(dim=1).numpy() + 1  # Convert back to 1-based indexing
    print("Predicted priority order:", pred_order)
