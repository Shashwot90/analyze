import gradio as gr
from theme_classifier import ThemeClassifier
import time

def get_themes(theme_list_str, subtitles_path, save_path):
    import time
    start_time = time.time()
    print("Process started...")  # Log when the process starts
    
    # Parse the theme list
    theme_list = theme_list_str.split(',')
    print(f"Parsed theme list: {theme_list}")  # Log the parsed theme list
    
    # Initialize the ThemeClassifier
    theme_classifier = ThemeClassifier(theme_list)
    print("Initialized ThemeClassifier.")  # Log initialization
    
    # Process the subtitles to get themes
    output_df = theme_classifier.get_themes(subtitles_path, save_path)
    print("Themes extracted.")  # Log after themes are extracted
    
    # Remove 'dialogue' from the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    print(f"Filtered theme list (removed 'dialogue'): {theme_list}")  # Log filtered theme list
    
    # Filter and aggregate the output dataframe
    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme', 'Score']
    print("Aggregated theme scores.")  # Log aggregation step
    
    # Create the bar plot
    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme", "Score"],
        vertical=False,
        width=500,
        height=260
    )
    print("Generated bar plot.")  # Log bar plot generation
    
    end_time = time.time()
    processing_time = end_time - start_time
    print(f"Processing complete. Total time: {processing_time:.2f} seconds")  # Log total processing time
    
    # Return the chart and the processing time
    return output_chart, f"Processing time: {processing_time:.2f} seconds"

# def get_themes(theme_list_str,subtitles_path,save_path):
#     start_time = time.time()
#     theme_list = theme_list_str.split(',')
#     theme_classifier = ThemeClassifier(theme_list)
#     output_df = theme_classifier.get_themes(subtitles_path,save_path)

#     # Remove dialogue from the theme list
#     theme_list = [theme for theme in theme_list if theme != 'dialogue']
#     output_df = output_df[theme_list]

#     output_df = output_df[theme_list].sum().reset_index()
#     output_df.columns = ['Theme','Score']

#     output_chart = gr.BarPlot(
#         output_df,
#         x="Theme",
#         y="Score",
#         title="Series Themes",
#         tooltip=["Theme","Score"],
#         vertical=False,
#         width=500,
#         height=260
#     )
#     end_time = time.time()
#     processing_time = end_time - start_time
#     print(processing_time)
#     return output_chart, f"Processing time: {processing_time:.2f} seconds"


def main():
    with gr.Blocks() as iface:
        # Theme Classification Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classification (Zero Shot Claasifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="Themes")
                        subtitles_path = gr.Textbox(label="Subtitles or script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button =gr.Button("Get Themes")
                        get_themes_button.click(get_themes, inputs=[theme_list,subtitles_path,save_path], outputs=[plot])

    iface.launch(share=True)
                
                
                
                
                
if __name__ == "__main__":
    main()