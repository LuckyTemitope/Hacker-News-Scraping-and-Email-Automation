import requests  # Http Requests
from bs4 import BeautifulSoup  # Web Scraping
import smtplib  # Email Body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# System Time and Date manipulation
import datetime

now = datetime.datetime.now()

# Email content holder
content = ''


# Extract Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    newsContent = ''
    newsContent += '<h1>Hacker News Top Stories:</h1>\n'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        newsContent += "<b>" + ((str(i + 1) + ')</b> ' + tag.text + '\n<br>') if tag.text != 'More' else '')
        # print(tag.prettify) #find all ('span', atttrs={'class': 'sitestr'}))
    return newsContent


newsContent = extract_news('https://news.ycombinator.com/')
content += newsContent
content += '<br>----------<br>'
content += '<br>End of Message<br><p style="font-family: courier; font-weight: lighter;">Lucky Osunbiyi</p>'

# Send the Email
print('Composing Email...')

# Update Email Details
SERVER = 'smtp.gmail.com'  # smtp server
PORT = 587  # port number
FROM = 'osunbiyi.temitope1@gmail.com'  # email id
TO = ['osunbiyi.temitope1@gmail.com']  # recipient email
PASS = ''  # email password

# fp = open(file_name, 'rb')
# Create a plain/text messsage
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'Top Hacker News Stories [Automated Email] ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)
msg['From'] = FROM
msg['To'] = ', '.join(TO)

msg.attach(MIMEText(content, 'html'))
# fp.close()

# Setup Server
print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
# server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent!!!')

server.quit()
