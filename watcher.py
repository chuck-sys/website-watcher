"""
The main file to run.
"""
import sys
import os
from typing import List, Dict, Tuple
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail

from config import WatcherConfig
from cache import WatcherCache
from entries import Entries


def main(args: List[str]):
    """The main function."""
    wconfig = WatcherConfig(os.environ)
    wcache = WatcherCache(wconfig)
    entries = Entries(wconfig, wcache, args[0])

    # Get the sites and compare
    comparisons = entries.get_comparison()

    # Send the email (if needed)
    if len(comparisons) > 0:
        send_email(wconfig, comparisons)
    else:
        print('No differences found; no need to send emails')

    # Write to cache for next time
    entries.write_to_cache()


def send_email(wconfig: WatcherConfig, comparisons: Dict[str, str]):
    """Sends the email."""
    client = sendgrid.SendGridAPIClient(api_key=wconfig.sendgrid_api)
    from_email = Email(wconfig.from_email)
    to_email = To(wconfig.to_email)
    subject = '[Automated] Websites Changed Notification'
    content = make_content(comparisons)
    mail = Mail(from_email, to_email, subject, content)
    response = client.client.mail.send.post(request_body=mail.get())

    if response.status_code // 100 == 2:
        print('Email sent!')
    else:
        print('Couldn\'t send email:')
        print(response.status_code)
        print(response.body.decode('utf-8'))



def make_single_item(item: Tuple[str, str]) -> str:
    """Create a single entry from an item (name, table)."""
    return f'''
<p><strong>{item[0]}</strong> <a href="{item[1][1]}">[website]</a></p>
<p>{item[1][0]}</p>
'''


def make_content(comparisons: Dict[str, str]) -> Content:
    """Create the content itself."""
    body = f'''
<style type="text/css">
table.diff {{font-family:Courier; border:medium;}}
.diff_header {{background-color:#e0e0e0}}
td.diff_header {{text-align:right}}
.diff_next {{background-color:#c0c0c0}}
.diff_add {{background-color:#aaffaa}}
.diff_chg {{background-color:#ffff77}}
.diff_sub {{background-color:#ffaaaa}}
</style>
<table class="diff" summary="Legends">
<tr> <th colspan="2"> Legends </th> </tr>
<tr> <td> <table border="" summary="Colors">
  <tr><th> Colors </th> </tr>
  <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
  <tr><td class="diff_chg">Changed</td> </tr>
  <tr><td class="diff_sub">Deleted</td> </tr>
</table></td>
<td> <table border="" summary="Links">
  <tr><th colspan="2"> Links </th> </tr>
  <tr><td>(f)irst change</td> </tr>
  <tr><td>(n)ext change</td> </tr>
  <tr><td>(t)op</td> </tr>
</table></td> </tr>
</table>
<p><strong>
There are {len(comparisons)} website(s) that have changed:
</strong></p>
{"<hl>".join([make_single_item(item) for item in comparisons.items()])}
'''
    return Content('text/html', body)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Missing 1 argument: CSV file')
    else:
        main(sys.argv[1:])
