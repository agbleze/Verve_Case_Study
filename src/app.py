#%%
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, dcc
from dash.exceptions import PreventUpdate
from helper_components import create_offcanvans, output_card, OptimalBidValuation
import pandas as pd
import numpy as np

#%% import win rate data 
data_win_rate = pd.read_csv('data_win_rate.csv')

#%%
app = dash.Dash(__name__, external_stylesheets=[
                                                dbc.themes.SOLAR,
                                                dbc.icons.BOOTSTRAP,
                                                dbc.icons.FONT_AWESOME,
                                            ]
                )


app.layout = html.Div([

    dbc.Row([
        html.Br(), html.Br(),
        dbc.Col(dbc.Button('Project description',
                           id='proj_desc',
                           n_clicks=0
                           )
            ),
        dbc.Col(children=[
                            html.Div(
                                    children=[create_offcanvans(id='project_canvans',
                                                                title='Optimal Bid price',
                                                                is_open=False
                                                            )
                                              ]
                                ),
                          ]
                )
    ]),
    dbc.Label("Determine Optimal bid price to send to auction based on advertiser pay"),
    html.Br(), html.Br(),
    
    
    dbc.Row([dbc.Col(md=4,
                     children=[dbc.Label('Select Advertiser pay'),
                         dcc.Dropdown(id='advertiser_pay',
                                                 placeholder='Amount Advertiser is willing to pay',
                                                options=[
                                                    {'label': f'$ {advert_pay}', 'value': advert_pay}
                                                    for advert_pay in np.arange(start=0.5, stop=50, step=0.5)
                                                ]
                                            )
                      ]
                     ),
             
             dbc.Col(md=4,
                     children=[
                                dbc.Label('Click button to compute optimal bid price'),
                                html.Br(),
                                dbc.Button(id='submit_parameters',
                                                children='Determine Optimal bid price'
                                                )
                                ]
                    ),
             
             dbc.Col(id='bidding',
                     children=[
                         
                         html.Div(id="bidding_div",
                                  children=[
                                      dbc.Label('Optimal bid price to send as response to auction'),
                                      output_card(id="bid_output",
                                                        card_label="Optimal bid"
                                                    )
                                            ]
                                  )
                     ]
                     ),
                       
            ]
            ),
    html.Br(), html.Br(),

    
    dbc.Row([
              dbc.Col([
                  dbc.Modal(id='missing_para_popup', is_open=False,
                      children=[
                      dbc.ModalBody(id='desc_popup')
                  ])
              ]
                      )
             ]
            )
])



@app.callback(Output(component_id='desc_popup', component_property='children'),
              Output(component_id='missing_para_popup', component_property='is_open'),
              Output(component_id='bid_output', component_property='children'),
              Input(component_id='submit_parameters', component_property='n_clicks'),
              Input(component_id='advertiser_pay', component_property='value'),
              )

def get_optimal_bidprice(submit_button: int, advertiser_pay: int):
    """
    This function accepts click events and advertiser pay to estimate the optimal 
    bidding price to send.

    Parameters
    ----------
    submit_button : int
        Number of times the submit button has been clicked.
    advertiser_pay : int
        This describes the amount an advertiser pay for their ads to be shown.
        
    Returns
    -------
    desc_popup: str
        This is a message in a popup component that is shown when no selection is made before clicking submit button.
    missing_para_popup: bool
        This is an output component that opens when selection is not made
        for all parameters before clicking submit buttion.
    bid_output
        This is an output component where optimal bid price is displayed.

    """
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'submit_parameters':
        if (not advertiser_pay):
            message = ('All parameters must be provided. Please select the \
                       right values for all parameters from the dropdown. \
                        Then, click on "Determine Optimal Bid price" button to compute \
                        the optimal bid valuation for the selected advertiser pay'
                       )
            return message, True, dash.no_update
        else:
            optimal_bid = OptimalBidValuation(data=data_win_rate)
            optimal_bid.compute_bid_value(advertiser_pay=advertiser_pay)
            optimal_bid_value = optimal_bid.compute_optimal_bid
            
            return dash.no_update, False, f'${optimal_bid_value}'



@app.callback(Output(component_id='project_canvans', component_property='is_open'),
              Input(component_id='proj_desc', component_property='n_clicks'),
              State(component_id='project_canvans', component_property='is_open')
              )
def toggle_project_description(proj_desc_button_clicked: str, is_open: bool) -> bool:
    """
    This function accepts click event input and the state of canvas component,
    and change the state of the canvans component when a click occurs

    Parameters
    ----------
    proj_desc_button_clicked : str
        This parameter is a count of each click made on a button.
    is_open : bool
        Has the values True or False that specifies whether the canvas component is opened or not.

    Returns
    -------
    bool
        Has values True or False that determines whether the canvans component should be open.

    """
    if proj_desc_button_clicked:
        return not is_open
    else:
        return is_open



if __name__ == '__main__':
    app.run_server(port=8023, debug=False, use_reloader=False)






