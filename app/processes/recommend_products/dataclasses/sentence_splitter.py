from pydantic import BaseModel, ConfigDict
from azure.ai.formrecognizer import DocumentParagraph
from typing import Any, List, Tuple
from collections import deque
import re
from math import ceil

class Splitter(BaseModel):
    def chunk(self,text):
