from backend.app.services.recommendations.trainer import run_training_2018_category_top

if __name__ == "__main__":
    result = run_training_2018_category_top(limit_per_category=20, metric="qty")
    print(result)

