
import time

import requests
import browsercookie

from bs4 import BeautifulSoup


# TODO: make sure you have already login-ed to the site on your browser
def main():
    base_url = "https://newark-tc-clients.winkcdn.com/public/dash/"
    # TODO: change below for a new camera location
    url = base_url+"WF05-A383-DCA2-04D6-3D74_cvp.mpd"

    # TODO: if you use a browser other than chrome, change the line below
    cookie = browsercookie.chrome()

    unique_urls = dict()

    with open('test.m4v', 'wb') as f:
        while True:
            r = requests.get(url, cookies=cookie, verify=False)
            soup = BeautifulSoup(r.text, 'lxml-xml')

            vid_init = soup.MPD.SegmentTemplate.attrs['initialization']
            print(vid_init)
            print(base_url+vid_init)
            r = requests.get(base_url+vid_init, cookies=cookie, verify=False)
            f.write(r.content)

            vid_template = soup.MPD.SegmentTemplate.attrs['media']

            timesteps = soup.MPD.SegmentTemplate.SegmentTimeline.findAll('S')
            for tt in timesteps:
                ts = tt.attrs['t']
                vid_url = vid_template.replace("$Time$", str(ts).strip())
                if vid_url in unique_urls:
                    continue
                unique_urls[vid_url] = True
                print(vid_url)
                print(base_url+vid_url)
                r = requests.get(base_url+vid_url, cookies=cookie, verify=False)
                f.write(r.content)

            time.sleep(1)





if __name__ == '__main__':
    main()

