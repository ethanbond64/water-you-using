import csv

def save_to_csv(articles, filename):
    keys = ['article_url', 'article_title', 'water_region', 'water_stress_severity']
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(articles)
