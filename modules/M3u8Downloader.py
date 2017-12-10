# (for py2 compatibility) encoding: utf-8
""" Functions to download an m3u8 playlist file """

from NetworkLayer import NetworkHandler
from GuiLib import get_quality_choice

def get_chunk_list(root, m3u8_link):
    """ This function will return a list of absolute links of all chunks for an m3u8 link """

    # Download playlist index:
    # The m3u8 link is to a file which has links to another m3u8 file for
    # all available qualities
    m3u8_file_list = NetworkHandler.get_instance().get_page(m3u8_link).splitlines()

    qualities = [quality.split(':')[1] for quality in m3u8_file_list if 'BANDWIDTH' in quality]
    links = [link  for link in m3u8_file_list if 'http' in link]

    idx = get_quality_choice(root, qualities)
    if idx is None:
        return None

    # Download the file and make a list of all chunks
    m3u8_playlist_file = NetworkHandler.get_instance().get_page(links[idx])
    # Base link for all chunks
    base_link = links[idx][:links[idx].rindex('/')+1]
    # All chunk are relative links
    # (filter empty lines and comments)
    chunk_list = [l for l in m3u8_playlist_file.splitlines() if l and l[0] != '#']
    # Add base link
    chunk_list = [base_link + l for l in chunk_list]

    return chunk_list

def download_m3u8_file(root, m3u8_link, dest_file_name, chunk_count_callback, curr_chunk_callback):
    """ Do the actual downloading """

    chunk_list = get_chunk_list(root, m3u8_link)
    if chunk_list is None:
        return False

    chunk_count_callback(len(chunk_list))
    # Open file and append all chunks to it
    with open(dest_file_name, 'wb') as dest_file:
        for idx, chunk in enumerate(chunk_list):
            chunk_bytes = NetworkHandler.get_instance().get_page_bytes(chunk)
            dest_file.write(chunk_bytes)
            curr_chunk_callback(idx)
    return True
