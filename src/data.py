import pandas as pd

def load_filtered_date():

    df = pd.read_excel("data/master_questions.xlsx", sheet_name="Sheet1")

    print(f'Column names of OG data : {df.columns}')
    
    required_cols = ['id', 'text', 'answer', 'difficulty', 'text.1']

    filter_df = df[required_cols]
    filter_df = filter_df.rename(columns = {
                                "id" : "question_id",  
                                "text" : "question_text", 
                                "answer" : "final_answer", 
                                "difficulty" : "difficulty",
                                "text.1" : "options_text"
                            })

    print(f'Column names of filtered data : {filter_df.columns}')

    return filter_df

