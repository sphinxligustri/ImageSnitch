# ImageSnitch
Find out where an image has been used on the internet.

# Prerequisites
* Register at (SerpApi)[https://serpapi.com/] and get yourself an API key.
* Bash
* Python

# Use
Use a link to a publicly accessible image to check for where it has been used on the internet.

```bash
api_key="<your API key>"
file_name="<A file with image links>"
target_dir="<where to store the results>"
bash snitch_on_links.sh ${api_key} ${file_name} ${target_dir}
```
