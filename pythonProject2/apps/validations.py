import re
from fastapi import status, HTTPException

from apps import common_constants


class RegexValidation:
    def __init__(self, field_data, regex_pattern, error_message):
        self.field_data = field_data
        self.regex_pattern = regex_pattern
        self.error_message = error_message

    video_mime_type_regex = common_constants.VIDEO_MIME_TYPE_REGEX

    def regex_validator(self):
        if re.fullmatch(self.regex_pattern, self.field_data):
            return self.field_data
        else:
            raise HTTPException(detail=self.error_message, status_code=status.HTTP_400_BAD_REQUEST)
