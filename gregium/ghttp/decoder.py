"""
Decoding for different types of data forms
"""
import logging

logger = logging.getLogger(__name__)

def strip_webform(response: "HTTPResponse") -> list[dict]:
    """
    Takes the data from a webform and returns a list of each segment

    Additional information (such as 'filename') in headers will be prefixed with a '*'
    """
    content_type = response.headers["Content-Type"]

    # Get boundary
    _, *cont_info = content_type.split("; ")

    boundary: bytes = (
        next(filter(lambda x: x.startswith("boundary="), cont_info))
        .lstrip("boundary=")
        .encode("utf-8")
    )

    # Split and clean up data
    if response.content.endswith(boundary + b"--"):
        data: list[bytes] = [x[2:-4] for x in response.content.split(boundary)[1:-1]]
    else:
        data: list[bytes] = [x[2:-4] for x in response.content.split(boundary)[1:]]

    # Read headers and content of each part of data
    form_data: list = []

    for packet in data:

        since_last = 0  # Every header in the data is split by a single line in between, the content has 3 lines between the last header & content

        content = b""

        packet_data = {}

        # Check each "line" in data
        for header in packet.split(b"\r\n"):

            if since_last == 1:

                # Once line has been found, add all data
                content += header + b"\r\n"

                continue

            # Read headers and update values
            if len(header) > 0:

                header_name, header_data = header.split(b": ")

                if header_name == b"Content-Disposition":

                    split_header_data = header_data.split(b"; ")

                    for split_header_item in split_header_data[1:]:

                        ds_header_name, ds_header_item = split_header_item.split(b"=")

                        packet_data["*" + ds_header_name.decode("utf-8")] = (
                            ds_header_item.decode("utf-8").strip('"')
                        )

                packet_data[header_name.decode("utf-8")] = header_data.decode("utf-8")

                since_last = 0

            else:

                since_last += 1

        packet_data["Content"] = content

        form_data.append(packet_data)

    return form_data

def load_cookies(cookies:str) -> dict[str,str]|None:
    """
    Loads a cookie string into a dictionary

    name1=value1; name2=value2 --> {"name1":"value1","name2":"value2"}

    In the case the cookies are formatted incorrectly, none will be returned
    """

    try:
        return dict([cookie.split("=") for cookie in cookies.split(";")])

    except Exception:
        logger.exception(f"Could not load cookies \"{cookies}\"")
        return None

def dump_cookies(data:dict[str,str]) -> str:
    """
    Converts a dictionary into a cookie string

    (Make sure data doesn't contain illegal characters like ';' or '=')
    
    {"name1":"value1","name2":"value2"} --> name1=value1; name2=value2
    """

    return "; ".join("=".join(item) for item in data.items())

from .connector import HTTPResponse