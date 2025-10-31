import pandas as pd
import numpy as np # 비어있는 값(NaN) 처리를 위해 import

def merge_and_clean():
    print("--- 1. 파일 불러오기 ---")
    try:
        df_aladin = pd.read_csv('aladin.csv', index_col=0, dtype={'item_id': str})
        print("aladin.csv 로드 완료 (index_col=0 사용).")
        df_aladin['category'] = df_aladin['category'].astype(object)

    except FileNotFoundError:
        print("오류: aladin.csv 파일을 찾을 수 없습니다.")
        print("먼저 1_crawl_bestsellers.py를 실행하세요.")
        return

    try:
        df_category = pd.read_csv('category_mapping.csv', dtype={'item_id': str})
        print("category_mapping.csv 로드 완료.")
    except FileNotFoundError:
        print("오류: category_mapping.csv 파일을 찾을 수 없습니다.")
        print("먼저 2_crawl_categories.py를 실행하세요.")
        return

    print("-" * 30)
    print("--- 2. 병합 및 카테고리 업데이트 ---")
    
    df_merged = pd.merge(
        df_aladin,
        df_category.drop_duplicates(subset=['item_id']), 
        on='item_id',
        how='left'
    )

    has_new_category = df_merged['real_category'].notnull() & (df_merged['real_category'] != 'N/A')
    
    print(f"{has_new_category.sum()}개 행의 카테고리를 업데이트합니다.")
    df_merged.loc[has_new_category, 'category'] = df_merged.loc[has_new_category, 'real_category']
    df_merged = df_merged.drop(columns=['real_category'])

    print("카테고리 열 업데이트 완료.")
    print("-" * 30)
    print("--- 3. 카테고리 없는 행 삭제 ---")

    condition_to_drop = (df_merged['category'].isnull()) | (df_merged['category'] == 'N/A')
    num_dropped = condition_to_drop.sum()
    df_cleaned = df_merged[~condition_to_drop]

    print(f"카테고리가 비어있거나 'N/A'인 {num_dropped}개 행을 삭제했습니다.")
    print(f"최종 데이터: {len(df_cleaned)}개")

    print("-" * 30)
    print("--- 4. 최종 파일 저장 ---")
    
    df_cleaned.to_csv('aladin_final_cleaned.csv', encoding='utf-8-sig', index=True)
    print("🎉 최종 파일 'aladin_final_cleaned.csv' 저장 완료.")

####################################################
if __name__ == "__main__": # 스크립트로 실행 시에만 작동
    merge_and_clean()
