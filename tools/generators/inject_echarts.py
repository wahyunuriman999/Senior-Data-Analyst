import urllib.request
import re

print('Downloading ECharts...')
url = 'https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    response = urllib.request.urlopen(req)
    echarts_js = response.read().decode('utf-8')
    print('Download complete. Injecting...')

    html_path = r'C:\Users\ROG G532 LV\.gemini\antigravity\brain\3ed9f1b4-c6cf-43cb-a6a5-3bdfd69ebeeb\apex_executive_sales_dashboard.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Hapus script lama
    pattern = r'<script src="https://cdn\.jsdelivr\.net[^>]+></script>'
    html = re.sub(pattern, '', html)

    # Sisipkan script baru sebelum tag <style>
    inline_script = f'<script>\n{echarts_js}\n</script>\n<style>'
    html = html.replace('<style>', inline_script)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print('Berhasil menyuntikkan 1MB ECharts langsung ke dalam HTML!')
except Exception as e:
    print('Error:', e)
