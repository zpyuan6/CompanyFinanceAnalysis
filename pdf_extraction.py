import os
import tabula
import pdfplumber
import pandas as pd
import logging
import tqdm

logging.basicConfig(level=logging.ERROR) 

"""
Install tabula-py, pdfplumber, pandas, tqdm by running the following commands in the terminal:
pip install pandas
pip install tabula-py
pip install pdfplumber
pip install tqdm
"""


if __name__ == "__main__":

    data = pd.DataFrame(columns=[
        "File Name", 
        "Operating profit befor tax this year",  
        "Operating profit befor tax last year", 
        "Operating expenses this year", 
        "Operating expenses last year", 
        "Cash and cash equivalents at the end of year this year", 
        "Cash and cash equivalents at the end of year last year", 
        "Total equity this year",
        "Total equity last year"])

    for root, folder, files in os.walk("C:\\Users\\zhipeng\\Desktop\\年报"):

        target_metrics = ["Operating profit befor tax", "Operating expenses", "Cash and cash equivalents at the end of year", "Total equity"]

        for file in files:

            save_information = {
                "File Name":-1, 
                "Operating profit befor tax this year":-1,  
                "Operating profit befor tax last year":-1, 
                "Operating expenses this year":-1, 
                "Operating expenses last year":-1, 
                "Cash and cash equivalents at the end of year this year":-1, 
                "Cash and cash equivalents at the end of year last year":-1, 
                "Total equity this year":-1,
                "Total equity last year":-1
            }

            if file.endswith(".pdf"):
                print(f"{file}=======================================")

                pdf = pdfplumber.open(f"{root}\\{file}")

                with tqdm.tqdm(total=len(pdf.pages)) as pbar:
                    for page in pdf.pages:
                        pbar.update(1)

                        text = page.extract_text()

                        if "Company statement of financial position" in text:
                            tables = tabula.read_pdf(f"{root}\\{file}", pages=page.page_number, multiple_tables=True)
                            for table in tables:
                                if len(table.columns.to_list())<=4 and len(table)>6:
                                    # print(table)
                                    # table.to_csv(f"extract_data_from_{file.split('.')[0]}_for_Company statement of financial position.csv", index=False)
                                    total_equity = table[table[table.columns[0]]=="Total equity"]
                                    if len(total_equity)>0:
                                        save_information["Total equity this year"] = total_equity[table.columns[-2]].values[0]
                                        save_information["Total equity last year"] = total_equity[table.columns[-1]].values[0]
                                        print("Total, ",total_equity)


                        if "Consolidated cash flow statement" in text:
                            tables = tabula.read_pdf(f"{root}\\{file}", pages=page.page_number, multiple_tables=True)
                            for table in tables:
                                if len(table.columns.to_list())<=4 and len(table)>6:
                                    # table.to_csv(f"extract_data_from_{file.split('.')[0]}_for_Consolidated cash flow statement.csv", index=False)
                                    cash = table[table[table.columns[0]]=="Cash and cash equivalents at the end of year"]
                                    
                                    if len(cash)>0:
                                        save_information["Cash and cash equivalents at the end of year this year"] = cash[table.columns[-2]].values[0]
                                        save_information["Cash and cash equivalents at the end of year last year"] = cash[table.columns[-1]].values[0]
                                        print("Cash, ",cash)


                        if "Consolidated statement of comprehensive income" in text:
                            tables = tabula.read_pdf(f"{root}\\{file}", pages=page.page_number, multiple_tables=True)
                            for table in tables:
                                if len(table.columns.to_list())<=4 and len(table)>6:
                                    # table.to_csv(f"extract_data_from_{file.split('.')[0]}_for_Consolidated statement of comprehensive income.csv", index=False)
                                    operating_expenses = table[table[table.columns[0]]=="Operating expenses"]
                                    operating_profit = table[table[table.columns[0]]=="Operating profit before tax"]
                                    
                                    if len(operating_expenses)>0:
                                        save_information["Operating expenses this year"] = operating_expenses[table.columns[-2]].values[0]
                                        save_information["Operating expenses last year"] = operating_expenses[table.columns[-1]].values[0]
                                        print("Expense, ",operating_expenses)
                                    if len(operating_profit)>0:
                                        save_information["Operating profit befor tax this year"] = operating_profit[table.columns[-2]].values[0]
                                        save_information["Operating profit befor tax last year"] = operating_profit[table.columns[-1]].values[0]
                                        print("Profit, ", operating_profit)
                                    

                save_information["File Name"] = file.split(".")[0]

                print(save_information)

                data.loc[len(data)]= save_information

    data.to_csv("data.csv", index=False)
            
            

