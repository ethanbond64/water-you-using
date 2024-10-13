def extract_article_data(soup, source_url):
    articles = []
    if "npr.org" in source_url:
        # Custom logic for NPR articles
        for article in soup.find_all('article'):
            try:
                article_url = article.find('a')['href']
                article_title = article.find('h2').text.strip()
                water_region = "Unknown"  # No clear region info from NPR by default
                water_stress_severity = "Unknown"  # No clear stress severity from NPR by default

                articles.append({
                    'article_url': article_url,
                    'article_title': article_title,
                    'water_region': water_region,
                    'water_stress_severity': water_stress_severity
                })
            except AttributeError:
                continue
    elif "nature.com" in source_url:
        # Custom logic for Nature articles
        for article in soup.find_all('article'):
            try:
                article_url = article.find('a')['href']
                article_title = article.find('h3').text.strip()
                water_region = article.find('span', class_='region').text.strip() if article.find('span', class_='region') else "Unknown"
                water_stress_severity = "Unknown"  # No clear stress severity on Nature by default

                articles.append({
                    'article_url': article_url,
                    'article_title': article_title,
                    'water_region': water_region,
                    'water_stress_severity': water_stress_severity
                })
            except AttributeError:
                continue
    # Add more conditions for different domains
    return articles
