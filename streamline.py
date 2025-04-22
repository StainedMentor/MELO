import os
import subprocess
import re

model_dir = "./log/state"
data_path = "./Data/amazon/grocery_ratings.csv"
results = []

# Przechodzimy po wszystkich plikach .pt
for filename in os.listdir(model_dir):
    if filename.endswith(".pt"):
        match = re.search(r"bert4rec_(\d+)_.*\.pt", filename)
        if not match:
            continue
        checkpoint_step = match.group(1)
        model_path = os.path.join(model_dir, filename)
        print(f"Testuję model: {filename}")

        command = [
            "python", "main.py",
            "--model=bert4rec",
            "--mode=amazon",
            f"--data_path={data_path}",
            "--val_size=1000",
            "--num_test_data=5000",
            "--load_pretrained_embedding=True",
            "--test",
            f"--checkpoint_step={checkpoint_step}"
        ]

        result = subprocess.run(command, capture_output=True, text=True)
        
        # Przykład: oczekujemy że RMSE wypisuje się jako np. "RMSE: 0.945"
        last_lines = result.stdout.strip().splitlines()[-10:]  # patrzymy na ostatnie kilka linii
        for line in last_lines:
            if "RMSE" in line:
                try:
                    rmse = float(re.search(r"RMSE[:=]\s*([\d.]+)", line).group(1))
                    results.append((filename, rmse))
                    print(f"  --> RMSE: {rmse}")
                except Exception as e:
                    print(f"Nie udało się sparsować RMSE dla {filename}: {e}")
                break

# Sortujemy i pokazujemy najlepsze
results.sort(key=lambda x: x[1])
print("\nTOP 5 najlepszych modeli:")
for fname, score in results[:5]:
    print(f"{fname}: RMSE = {score}")
