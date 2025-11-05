"""
Module for creating dataset annotations
"""

import pandas as pd
import os
from typing import List, Dict
from data_processor import CurrencyDataProcessor


def create_annotation_file(dataset_path: str, annotation_file: str) -> bool:
    """
    Create annotation file for dataset
    
    Args:
        dataset_path: Path to dataset file or directory
        annotation_file: Path to output annotation file
        
    Returns:
        True if successful
    """
    try:
        annotation_data = []
        
        if os.path.isfile(dataset_path):
            # Single file dataset
            df = pd.read_csv(dataset_path)
            annotation_data.append({
                'filename': os.path.basename(dataset_path),
                'records_count': len(df),
                'date_from': df['date'].min(),
                'date_to': df['date'].max()
            })
        elif os.path.isdir(dataset_path):
            # Directory with multiple files
            for file in os.listdir(dataset_path):
                if file.endswith('.csv'):
                    filepath = os.path.join(dataset_path, file)
                    df = pd.read_csv(filepath)
                    annotation_data.append({
                        'filename': file,
                        'records_count': len(df),
                        'date_from': df['date'].min(),
                        'date_to': df['date'].max()
                    })
        else:
            print(f"Invalid dataset path: {dataset_path}")
            return False
        
        # Create annotation DataFrame and save
        annotation_df = pd.DataFrame(annotation_data)
        annotation_df.to_csv(annotation_file, index=False)
        print(f"Annotation created: {annotation_file}")
        return True
        
    except Exception as e:
        print(f"Error creating annotation: {e}")
        return False


def create_reorganized_dataset(source_path: str, target_dir: str, 
                             organization_type: str = "yearly") -> str:
    """
    Create reorganized dataset with specified organization
    
    Args:
        source_path: Path to source dataset
        target_dir: Target directory for reorganized dataset
        organization_type: Type of organization ('yearly', 'weekly', 'xy')
        
    Returns:
        Path to created dataset directory
    """
    try:
        os.makedirs(target_dir, exist_ok=True)
        processor = CurrencyDataProcessor(source_path)
        
        if organization_type == "yearly":
            created_files = processor.split_by_years(target_dir)
            print(f"Created {len(created_files)} yearly files")
        elif organization_type == "weekly":
            created_files = processor.split_by_weeks(target_dir)
            print(f"Created {len(created_files)} weekly files")
        elif organization_type == "xy":
            x_file = os.path.join(target_dir, "X.csv")
            y_file = os.path.join(target_dir, "Y.csv")
            processor.split_to_x_y(x_file, y_file)
            created_files = [x_file, y_file]
            print("Created X and Y files")
        else:
            print(f"Unknown organization type: {organization_type}")
            return ""
        
        return target_dir
        
    except Exception as e:
        print(f"Error creating reorganized dataset: {e}")
        return ""


if __name__ == "__main__":
    """Test annotation creator functionality"""
    # Test with single file
    create_annotation_file("dataset.csv", "original_annotation.csv")
    
    # Test with directory
    create_reorganized_dataset("dataset.csv", "test_yearly", "yearly")
    create_annotation_file("test_yearly", "yearly_annotation.csv")