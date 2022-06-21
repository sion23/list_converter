import io
import pandas as pd
import numpy as np
import ipywidgets as widgets


def prompt_upload():
    print('Upload Coding Confirmation (.xlsx)')
    uploader = widgets.FileUpload(accept='*.xlsx', multiple=False)
    display(uploader)

    main_display = widgets.Output()

    def on_upload_change(inputs):
        with main_display:
            main_display.clear_output()
            display(list(inputs['new'].keys())[-1])

    uploader.observe(on_upload_change, names='value')
    return [uploader, main_display]

def load_from_widget(uploader_in, header=5, sheet_name="AE"):
    '''
    Release function to load file
    '''
    uploaded_file = uploader_in.value
    file_name = list(uploaded_file.keys())[0]
    df = pd.read_excel(io.BytesIO(uploaded_file[file_name]["content"]),
                       header=header,
                       sheet_name=sheet_name)
    
    colnames = ["이상사례명(MedDRA_SOC_ENG)","이상사례명(MedDRA_SOC_KOR)",
            "이상사례명(MedDRA_PT_ENG)","이상사례명(MedDRA_PT_KOR)",
            "Expectedness","차수","중대성","ADR 여부", "자료원"]
    
    df = df[colnames]
    
    df["SOC"] = df["이상사례명(MedDRA_SOC_ENG)"] + " (" + df["이상사례명(MedDRA_SOC_KOR)"] + ")"
        
    df["PT"] = df["이상사례명(MedDRA_PT_ENG)"] + " (" + df["이상사례명(MedDRA_PT_KOR)"] + ")"
    df = df.drop(columns=["이상사례명(MedDRA_SOC_ENG)",
                              "이상사례명(MedDRA_SOC_KOR)",
                              "이상사례명(MedDRA_PT_ENG)","이상사례명(MedDRA_PT_KOR)"])
    
    
    return df
    
    

def load_format(filename, header=5, sheet_name="AE"):
    '''
    Debugging function to load file
    '''
    
    df = pd.read_excel(filename, header=5, sheet_name="AE")
    
    colnames = ["이상사례명(MedDRA_SOC_ENG)","이상사례명(MedDRA_SOC_KOR)",
            "이상사례명(MedDRA_PT_ENG)","이상사례명(MedDRA_PT_KOR)",
            "Expectedness","차수","중대성","ADR 여부", "자료원"]
    
    df = df[colnames]
    
    df["SOC"] = df["이상사례명(MedDRA_SOC_ENG)"] + " (" + df["이상사례명(MedDRA_SOC_KOR)"] + ")"
        
    df["PT"] = df["이상사례명(MedDRA_PT_ENG)"] + " (" + df["이상사례명(MedDRA_PT_KOR)"] + ")"
    df = df.drop(columns=["이상사례명(MedDRA_SOC_ENG)",
                              "이상사례명(MedDRA_SOC_KOR)",
                              "이상사례명(MedDRA_PT_ENG)","이상사례명(MedDRA_PT_KOR)"])
    
    
       
    return df


def process_values(df):
    binary_cols = ["Expectedness","중대성", "ADR 여부", "자료원"]
    edited = list()
    idx = 0
    while idx < len(binary_cols):
        cleaned = [x for x in df[binary_cols[idx]] if str(x) != 'nan']
        if len(pd.unique(cleaned)) > 2:
            print("Column '{}' is not binary: ".format(binary_cols[idx]), end="")
            print(pd.unique(cleaned))

            choice = input("\tSelect the following option:\n\t1) Remove rows with specified characters (제외할 경우) \n\t2) Replace specific characters (오타인 경우) \n\t3) Correct. Next \n\tNumber: ")
            
            if choice == "1":
                edited.append(idx)
                problem_rows = input("\t\tRemove rows with (exact) match:" )
                df = df.loc[~df[binary_cols[idx]].str.contains(problem_rows)]
                
                cleaned = [x for x in df[binary_cols[idx]] if str(x) != 'nan']
                if len(pd.unique(cleaned)) > 2:
                    print("Failed to make binary variable for '{}'".format(binary_cols[i]))
                    print(pd.unique(cleaned))
                    df = process_values(df)

            elif choice == "2":
                edited.append(idx)
                remove = input("\tString to remove (e.g., \\n): ")
                value = input("\tValue to replace: ")
                df[binary_cols[idx]] = df[binary_cols[idx]].str.replace(remove, value)
                
                cleaned = [x for x in df[binary_cols[idx]] if str(x) != 'nan']
                if len(pd.unique(cleaned)) > 2:
                    print("Failed to make binary variable for '{}'".format(binary_cols[i]))
                    print(pd.unique(cleaned))
                    df = process_values(df)
                
            elif choice == "3":
                idx += 1
                continue
                
            else:
                print("Enter 1, 2 or 3")
                idx -= 1
        idx += 1
            
    # for i in edited:
    #     cleaned = [x for x in df[binary_cols[i]] if str(x) != 'nan']
    #     if len(pd.unique(cleaned)) > 2:
    #         print("Failed to make binary variable for '{}'".format(binary_cols[i]))
    #         print(pd.unique(cleaned))
    #         print("Halting")
    #         assert False
        
    print("*"*40)
    print("Summary")
    for binary in binary_cols:
        print("{} : {}".format(binary, pd.unique(df[binary])))
    print("*"*40)
    
    return df


def process_time(df):
    choice = ""
    while (choice != "3"):
        print("Check if 차수 is correct:\n")
    
        print(pd.unique(df["차수"]), end='\n\n')
        choice = input("\tSelect the following option:\n\t1) Remove rows with specified characters (제외할 경우) \n\t2) Replace specific characters (오타인 경우) \n\t3) Correct. Next \n\tNumber: ")
        if choice == "1":
            problem_rows = input("\t\tRemove rows with (exact) match:" )

            print("*"*40)
            print("Removing following rows...\n")
            print("{}\n\n".format(df.loc[df["차수"].str.contains(problem_rows)]))
            print("*"*40)

            df = df.loc[~df["차수"].str.contains(problem_rows)]

        elif choice == "2":
            remove = input("\tCharacter(s) to replace (e.g., \\n): ")
            value = input("\tReplacement character(s): ")
            df["차수"] = df["차수"].str.replace(remove, value)
            
        elif choice == "3":
            continue
            
        else:
            print("Enter 1, 2 or 3")

    
    return df


def identify_adr(df):
    '''
    Identifies ADF여부 values (e.g., \"non-ADR\" vs. \"non ADR\")
    '''
    adr_stat = pd.unique(df["ADR 여부"])
    # adr_stat = ["ADR positive", "ADR negative"]
    
    if len(adr_stat) == 1:
        if "non" in adr_stat[0]:
            return 0
        else:
            return -1

    found = False
    non_idx = -1
    for i in range(2):
        if "non" in adr_stat[i]:
            found = True
            non_idx = i

    if not found:
        print("'ADR 여부' column에서 'ADR', 'non-ADR'을 찾지 못함:")
        print("현재 ADR 여부 column:")
        print(adr_stat)
        print("직접 ADR을 선택해주세요")
        truth = input("'{}'이 ADR 맞을까요? (혹은 '{}'이 non-ADR). Type y/n".format(adr_stat[0], adr_stat[1]))
        if truth:
            non_idx = 1
        else:
            non_idx = 0
    return non_idx


def make_expectedness_key(df):
    '''
    Works with data_processed     
    '''
    df["SOC-PT"] = df["SOC"] + "-" + df["PT"]
    key = df.drop(columns=['차수', '중대성', 'ADR 여부', '자료원', 'SOC', 'PT']).reset_index(drop=True)
    key = key.drop_duplicates("SOC-PT")
    key_cols = key['SOC-PT']
    key = key.T
    key.columns = key_cols
    key = key.reset_index(drop=True)
    key = key.drop(index=1)
    return key


def make_medDRA_key(df):
    key = df[["SOC-PT original", "SOC-PT"]]
    key = key.drop_duplicates("SOC-PT")
    key_cols = key['SOC-PT']
    key = key.T
    key.columns = key_cols
    key = key.reset_index(drop=True)
    key = key.drop(index=1)
    return key


def transform_format(data_processed_in, mode=0):
    '''
    mode = 0 : SOC and PT 합치 된 포맷 (합계 포함)
    mode = 1 : SOC and PT 분리 된 포맷 (default)
    '''
    data_processed_in = data_processed_in.copy()
    data_processed_in["SOC-PT original"] = data_processed_in["SOC"] + "-" + data_processed_in["PT"]
    data_processed_in["SOC"] = data_processed_in["SOC"].apply(lambda x : "".join(x.split()))
    data_processed_in["PT"] = data_processed_in["PT"].apply(lambda x : "".join(x.split())) 
    data_processed_in["SOC-PT"] = data_processed_in["SOC"] + "-" + data_processed_in["PT"]
    
    m_key = make_medDRA_key(data_processed_in)

    data_processed_in = data_processed_in.sort_values(["SOC", "PT"])
    table = data_processed_in.groupby(["SOC", "PT", "ADR 여부",
                                "차수", "중대성", "자료원"]).count().unstack(level=-2,
                                                                     fill_value=0).unstack(level=-2,
                                                                                           fill_value=0).unstack(level=-2,
                                                                                                                 fill_value=0)["Expectedness"]
    
    non_adr = identify_adr(data_processed_in)
    seriousness = pd.unique(data_processed_in["중대성"])
    time = pd.unique(data_processed_in["차수"])
    
    if len(pd.unique(data_processed_in["ADR 여부"])) == 1:
        if non_adr == -1:
            non_adr = 1
            adr = 0
            adr_status = [pd.unique(data_processed_in["ADR 여부"])[0], "non-ADR"]
            for s in seriousness:
                for t in time:
                    table[s, t, "non-ADR"] = 0
        else:
            adr = 1
            adr_status = [pd.unique(data_processed_in["ADR 여부"])[0], "ADR"]
            for s in seriousness:
                for t in time:
                    table[s, t, "ADR"] = 0
        
        
    else:
        adr_status = pd.unique(data_processed_in["ADR 여부"])
        
        if non_adr == 1:
            adr = 0
        else:
            adr = 1
            
    print("In {} ADR: '{}' NON-ADR: '{}'".format(adr_status, adr_status[adr], adr_status[non_adr]))
    
    # Since non-ADR (i.e., AE) includes ADR events too. Add ADR events to non-ADR events 
    for s in seriousness:
        for t in time:
            table[s, t, adr_status[non_adr]] = np.array(table[s, t, adr_status[non_adr]]) + np.array(table[s, t, adr_status[adr]])
    
    
    # Add expectedness column
    table_df = table.reset_index()
    table_df['SOC-PT'] = table_df['SOC'] + '-' + table_df['PT']
    
    e_key = make_expectedness_key(data_processed_in)
    table["Expectedness"] = e_key[table_df["SOC-PT"]].values[0]    
    
    if mode == 1:
        return table
    
    
    # Merge PT and SOC into one column
    table_df = table.reset_index()
    table_df['SOC-PT'] = table_df['SOC'] + '-' + table_df['PT']
    table_df['SOC-PT original'] = m_key[table_df["SOC-PT"]].values[0]
    table_df[['SOC', 'PT']] = table_df['SOC-PT original'].str.split('-', 1, expand=True)
    table_df["stat"] = 1
    sum_stat = table_df.groupby("SOC").sum()
    sum_stat["Expectedness"] = ""
    sum_stat["자료원"] = ""
    sum_stat["stat"] = 0
    sum_stat = sum_stat.reset_index()
    sum_stat["PT"] = sum_stat["SOC"]
    
    combined = pd.concat([table_df, sum_stat]).reset_index(drop=True)
    combined = combined.sort_values(["SOC", "stat"]).reset_index(drop=True)
    combined = combined.drop(columns=["SOC", "stat", "SOC-PT", "SOC-PT original"])    
    return combined


def control_process(uploader, main_display, option):
    if main_display:
        print("File submitted...")
        data = load_from_widget(uploader)
        data_binary = process_values(data)
        data_processed = process_time(data_binary)
        final = transform_format(data_processed, option)
        return final
    else:
        print("File not recognized")