import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

class ToolsBox:
    """
    Instance de la classe 
    >>
    from DataToolsBox import ToolsBox
    toolBox = ToolsBox(url_dataframe)
    <<
    """
    def __init__(self, dataset):
        """
        Lecture du dataset format : gz, zip, csv, xlsx
        """
        # Read DataFrame from a file
        if dataset.split(".")[-1] == 'gz':
            self.df = pd.read_csv(dataset, sep = '\t', compression='gzip', low_memory=False)
        elif dataset.split(".")[-1] == 'zip':
            self.df = pd.read_csv(dataset, compression='zip', low_memory=False)
        elif dataset.split(".")[-1] == 'csv':
            self.df = pd.read_csv(dataset, low_memory=False)
        elif dataset.split(".")[-1] == 'xlsx':
            self.df = pd.read_excel (dataset, low_memory=False)

        # Store columns names
        if "Unnamed: 0" in self.df.columns:
            self.df.drop(columns="Unnamed: 0", inplace=True)

        # Get numercic columns
        self.numeric_df = self.df.select_dtypes(include='number')

        # Relative path to folder where export_csv will save the CSV file
        self.export_folder = './exported_csv/'

    def test_method(self):
        return self.df.describe(include="all").T()

    def dtx_describe(self, col_names=None):
        # Définition de la méthode
        if col_names is not None:
            df = self.df[col_names]
        else:
            df = self.df
        df_describe = df.describe(include="all").T

        # Treating exeptions
        re_order = ["count", "Uniques_calc", "%NaN", "%Duplicate"]
        if "top" in df_describe:
            df_describe["top"] = df_describe["top"].apply(lambda top_content: top_content if type(top_content) != str else (str(top_content[30])+"..." if len(top_content) >= 30 else top_content))
            col_list = ["top", "freq"]
            for col in col_list:
                re_order.append(col)
        if "mean" in df_describe:
            col_list = ["mean", "std", "min", "25%", "50%", "75%", "max"]
            for col in col_list:
                re_order.append(col)
            
        df_describe["%NaN"] = df.apply(lambda columns : (columns.isna().sum() / len(columns))*100)
        df_describe["%Duplicate"] = df.apply(lambda columns : (columns.duplicated().sum() / len(columns)) * 100).round(2)
        df_describe["Uniques_calc"] = df.apply(lambda columns : len(columns.unique()))
        df_describe = df_describe[re_order]
        # df_describe = df_describe.style.apply(lambda column : ["background : darkred" if value > 0 else "" for value in column], subset=["%NaN", "%Duplicate"])

        return df_describe.round(2)

    def print_correlations(self):
        # Flatenand,remove self-correlations
        flat_corr = self.numeric_df.corr().unstack()
        strong_corr = flat_corr[flat_corr != 1].drop_duplicates()

        # Filter correlations that are stronger than the mean positive or mean negative
        strong_positive_corr = strong_corr[(strong_corr >= 0.5)].sort_values(ascending=False)
        litle_positive_corr = strong_corr[(strong_corr > 0.25) & (strong_corr < 0.5)].sort_values(ascending=False)

        strong_negative_corr = strong_corr[(strong_corr <= -0.5)].sort_values()
        little_negative_corr = strong_corr[(strong_corr < -0.25) & (strong_corr > -0.5)].sort_values()

        none_positive_corr = strong_corr[(strong_corr <= 0.25)].sort_values(ascending=False)
        none_negative_corr = strong_corr[(strong_corr >= -0.25)].sort_values()

        # results
        separator = "-----------------------------------------------------------"
        print(separator)
        print("Strongest Positive Correlations:")
        if len(strong_positive_corr) > 1:
            print(strong_positive_corr, "\n")
        else:
            print("There is no any Strong Positive Correlation", len(strong_positive_corr))
        print(separator)
        print()
        print(separator)
        print("Little Positive Correlations:")
        if len(litle_positive_corr) > 1:
            print(litle_positive_corr, "\n")
        else:
            print("There is no any Little Positive Correlation")
        print(separator)
        print()
        print(separator)
        print("Strongest Negative Correlations:")
        if len(strong_negative_corr) > 1:
            print(strong_negative_corr, "\n")
        else:
            print("There is no any Strongest Negative Correlation")
        print(separator)
        print()
        print(separator)
        print("Little Negative Correlations:")
        if len(little_negative_corr) > 1:
            print(little_negative_corr, "\n")
        else:
            print("There is no any Little Negative Correlation")
        print(separator)
        print()
        print(separator)
        print("None Correlations:")
        if len(none_positive_corr) > 1 and len(none_positive_corr) > 1 :
            print(none_positive_corr)
            print(none_negative_corr, "\n")
        else:
            print("There is no any None Correlation")
        print(separator)

    def correlations_map(self):
        correlation_matrix = self.numeric_df.corr()

        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,  fmt=".2f", linewidths=.5)
        plt.title('Correlation Numeric Features')

        return plt.show()

    def histplot(self, df=None, col_names=None):
        if df is None:
            df = self.df
        if col_names is None:
            col_names = self.numeric_df
        for col_name in col_names:
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col_name].dropna(), kde=True, bins=30)
            plt.title(f'Distribution of {col_name}')
            plt.xlabel(col_name)
            plt.ylabel('Frequency')
            plt.show()

    def boxplots(self, df=None, col_names=None, outlier=None):
        # Set df if not specified
        if df is None:
            df = self.df
        else:
            df = df
        # Set col_names if not specified
        if col_names is None:
            col_names = self.numeric_df

        # Iteration for columns
        for col_name in col_names:
            # Use outliers_filter if specified
            if outlier:
                x_values = self.outliers_filter(col_name)
            else:
                x_values = df[col_name]

            plt.figure(figsize=(10, 2))
            sns.boxplot(x=x_values.dropna())
            plt.title(f'Box Plot of {col_name}')
            plt.xlabel(col_name)
            plt.show()

    def cat_barplot(self, df=None, cat_col=None, col_values=None):
        # Set df if not specified
        if df is None:
            df = self.df
        else:
            df = df
        sns.barplot(data=df,y=cat_col,x=col_values,orient= 'h')

    def visualize_means_stacked_bar(df, group_column, exclude_cols):

        numeric_cols = df.select_dtypes(include=['number']).columns
        numeric_cols = [col for col in numeric_cols if col not in exclude_cols]

        pnns_groups = df[group_column].dropna().unique()

        means_data = pd.DataFrame()

        for group in pnns_groups:
            group_df = df[df[group_column] == group]
            mean_values = group_df[numeric_cols].mean()
            means_data[group] = mean_values

        means_data = means_data.transpose()
        means_data.plot(kind='barh', stacked=True, figsize=(12, 8))
        plt.title('Features by PNNS Group')
        plt.xlabel('PNNS Group')
        plt.ylabel('Mean Values')
        plt.legend(title='Numeric Features')
        plt.tight_layout()
        plt.show()

    def cat_countplot():
        # nutrition_grades_sorted = df_food['nutrition_grade_fr'].dropna().unique()
        # nutrition_grades_sorted = sorted(nutrition_grades_sorted)

        # color_dict = {
        #     'a': 'green',
        #     'b': 'lightgreen',
        #     'c': 'yellow',
        #     'd': 'orange',
        #     'e': 'red'}

        # plt.figure(figsize=(10, 6))
        # sns.countplot(x='nutrition_grade_fr', data=df_food, order=nutrition_grades_sorted, palette=color_dict)

        # plt.title('Distribution of Items by Nutrition Grade (FR)')
        # plt.xlabel('Nutrition Grade')
        # plt.ylabel('Number of Items')

        # plt.show()
        return None
    
    def multi_cat_barplot():
        # grade_counts = df_food.groupby(['pnns_groups_1', 'nutrition_grade_fr']).size().reset_index(name='count')

        # total_counts = df_food.groupby('pnns_groups_1').size().reset_index(name='total')
        # grade_counts = grade_counts.merge(total_counts, on='pnns_groups_1')

        # grade_counts['percentage'] = grade_counts['count'] / grade_counts['total'] * 100

        # plt.figure(figsize=(18, 8))
        # sns.barplot(x='pnns_groups_1', y='percentage', hue='nutrition_grade_fr', data=grade_counts,
        #             palette=color_dict, order=df_food['pnns_groups_1'].value_counts().index)

        # plt.title('Percentage of Nutrition Grades in Each PNNS Group 1')
        # plt.xlabel('PNNS Group 1')
        # plt.ylabel('Percentage of Nutrition Grade')
        # plt.legend(title='Nutrition Grade', loc='upper right')

        # plt.tight_layout()
        # plt.show()
        return None


    def multi_lineplot(self, df, cols):
        """
        ICheck if all value are unique or not
        """
        plt.figure(figsize=(8, 6))
        plt.title("KNN: Varying Number of Neighbors")
        plt.plot(df, cols.values(), label="Training Accuracy")
        plt.plot(df, cols.values(), label="Testing Accuracy")
        plt.legend()
        plt.xlabel("Number of Neighbors")
        plt.ylabel("Accuracy")
        plt.show()


    def unicite(self, col_names=None):
        """
        ICheck if all value are unique or not
        """
        if col_names is None:
            col_names = self.numeric_df
            df = self.df
        else:
            df = self.df
        for col_name in col_names:
            recurrence = df[col_name].value_counts().unique()
            if (recurrence[0] == 1)  :
                print (f'Values in {col_name} ARE unique.')
            else :
                print (f'Values in {col_name} are NOT unique.')

    def outliers_filter(self, col_name, df=None, outer=None, z_score=None):
        """
        Filter outliers of a column and return the DataFrame with outliers
        """
        # Set df if not specified
        if df is None:
            df = self.df
        else:
            df = df

        if col_name not in self.df.columns:
            raise ValueError("Column '{}' does not exist in the DataFrame.".format(col_name))

        if z_score :
            # Use Z_score with specified value
            z = stats.zscore(self.df[col_name])
            if outer:
                temp_df = self.df.loc[(z <= -z_score) | (z >= z_score)].sort_values(by=col_name, ascending=False)
                return temp_df
            else:
                temp_df = self.df.loc[(z > -z_score) & (z < z_score)].sort_values(by=col_name, ascending=False)
                return temp_df
        else:
            q1 = self.df[col_name].quantile(0.25)
            q3 = self.df[col_name].quantile(0.75)
            iq = q3-q1
            qmin = q1 - (1.5 * iq)
            qmax = q3 + (1.5 * iq)

            if outer:
                temp_df = self.df.loc[(self.df[col_name] < qmin ) | (self.df[col_name] > qmax)].sort_values(by = col_name, ascending = False)
            else:
                temp_df = self.df.loc[(self.df[col_name] > qmin ) | (self.df[col_name] < qmax)].sort_values(by = col_name, ascending = False)

        return temp_df

    # Fonction pour exporter le fichier CSV
    def export_csv(self, df,name_file):
            src = self.export_folder
            os.makedirs(src, exist_ok=True)  
            df.to_csv(src+name_file+'.csv')