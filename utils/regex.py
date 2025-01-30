import re 

def remove_table_and_text(text):
    pattern = r"#table.*"
    if not re.search(pattern, text, re.DOTALL):
        return False  
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL).strip()
    return cleaned_text

def remove_unnecesery_table(text):
    result = re.sub(r'\|.*', '', text).strip()
    return result 

def extract_sql_query(text):
    """Extract and clean up SQL query from the response text"""
    match = re.search(r'```sql\n(.*?)```', text, re.DOTALL)
    if match:
            return match.group(1).strip()
    return None
import re

def detect_none_in_text(text: str) -> bool:
    if not text: 
        return False
    
    pattern = r"None"
    return bool(re.search(pattern, text))
