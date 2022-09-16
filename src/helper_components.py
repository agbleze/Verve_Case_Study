from dash import dcc, html
import dash_bootstrap_components as dbc
from style import cardbody_style, card_icon, cardimg_style, card_style
import pandas as pd



def output_card(id: str = None, card_label: str =None,
                style={"backgroundColor": 'yellow'},
                icon: str ='bi bi-cash-coin', card_size: int = 4):
    return dbc.Col(lg=card_size,
                    children=dbc.CardGroup(
                        children=[
                            dbc.Card(
                                    children=[
                                        dcc.Loading(type='circle', children=html.H3(id=id)),
                                        html.P(card_label)
                                    ]
                                ),
                            dbc.Card(
                                    children=[
                                        html.Div(
                                            className=icon,
                                            style=card_icon
                                        )
                                    ],
                                    style=style
                            )
                        ]
                    )
                )


def create_offcanvans(id: str, title: str, is_open=False):
    return html.Div(
        [
            dbc.Offcanvas(
                id=id,
                title=title,
                is_open=is_open,
                children=[
                    dcc.Markdown('''
                                    #### Project description

                                    The aim of this task is to provide a convenient tool, that 
                                    enables the determination of the most optimal bid price to maximize net revenue,  
                                    to Verve Group.
                                    
                                    
                                    #### Features 
                                    
                                    Expected payoff (bid valuation): is computed using parameters such as win rate and net revenue   
                                    Bid valuation which determines the optimal bid price is the product of win rate and net revenue.
                                    
                                    Net revenue: is defined as the differences between what advertiser pays and bid price 
                                    that was paid to win the auction. By this, the bid price is required to be 
                                    lower than the advertiser pay.
                                    
                                    
                                    Optimal bid price: is equivalent to the bid price with maximum expected payoff / bid valuation


                                    #### Assumptions
                                    
                                    1. This is a first price auction where the winner is determined as the higest bidder and 
                                    pays the winning bidding price
                                    
                                    
                                    
                                    2. Revenue is only made when Verve Group successfully bids (wins the bid) at a price lower 
                                    than what the advertiser paid 
                                    
                                    3. It is assumed that the number of events for which a response is bid is representative of 
                                    all possible occurence and outcome for a bid price. Win rate for a bid price is robust against 
                                    and independent of number of events for a bid price. Thus, the sample size of the events for each 
                                    bid price is adequate and does not influence the win rate when more bids are made. This is an 
                                    assumption that is quite extreme. Example the win rate of $1.0 which was bidded 600 times is about 60% compare 
                                    to 30% for $0.1 which was bidded 3000 times. The difference in number of times these bid prices were 
                                    bidded is assumed to not account for the difference in win rate. 
                                    
                                    4. The goal of bidding with the optimal bid price which is to maximize revenue is achieve by choosing 
                                    the lowest bid price less than the advertiser pay that has the highest win rate.
                                    
                                    
                                    #### Algorithm for estimating optimal bid price
                                    
                                    Based on the available data, each time a different advertiser price is selected, the 
                                    following procedure is used to estimate the extected payoff / bidding valuation and 
                                    based on that the optimal bid price is selected;
                                    
                                    1. Estimate expected win rate for a bid price based on selected advertiser pay 

                                    In order to estimate the win rate, the following procedures are identified
                                    
                                    (i) Estimate total wins recorded for bidding at a given bid price (total bid wins): 
                                    This information can be retrieve from the table provided.
                                    A simple process is to filter the data to the given bid price for which win 
                                    rate is to be estimated, and select number of times (events column) a win occured (win = 1)

                                    (ii) Estimate total number of times a bid was placed at a given bid price (total bids): 
                                    This is estimated by filtering the data to a given bid price and finding the sum of events. 
                                    This is equivalent to sum of events for both bid wins and losses for a given bid price

                                    (iii) Estimate win rate to be given as (total wins / total bids)
                                    
                                    
                                    2. Estimate expected payoff and determine optimal bid price
                                    
                                    (iv) Compute net revenue (advertiser pay - winning bid price)
                                    
                                    (v) Compute the expected payoff (also termed bid valuation in this exercise) with the formula below;
                                    
                                    Expected payoff (bidding valuation) = win rate * net revenue

                                    Optimal bid price = bid price of maximum expected payoff


                                    #### Tools used
                                    
                                    Among others, libraries and packages used included the following

                                    * Pandas
                                    * Numpy
                                    * Dash to build this web application


                                    #### Project output
                                    
                                    - Web application
                                    
                                    With the user interface provided here, various advertiser pay
                                    can be selected and the optimal bid price is determined as the output
                                
                                '''
                                )
                    ]
            ),
        ]
    )



class OptimalBidValuation:
    """This class provides various methods to compute expected payoff or bid value and 
        optimal bid price
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    ## function to estimate bid valuation for various bid prices
    
    def compute_bid_value(self, advertiser_pay: int=0.5, 
                    bid_price_column: str = 'bid_price', 
                    win_rate_column: str = 'win_rate') -> pd.DataFrame:
        """This function accepts advertiser price, column names for 
        the bid price and win rate to compute the bid value which is the expected payoff.

        Args:
            advertiser_pay (int, optional): This is the how much the advertiser is paying for ad. Defaults to 0.5.
            bid_price_column (str, optional): This is a column containing the price at which a bid is made. Defaults to 'bid_price'.
            win_rate_column (str, optional): This is a column name containing the rate at which bid price is successful. Defaults to 'win_rate'.

        Returns:
            pd.DataFrame: Dataframe containing data on advertiser pay, bid price and estimated bid value which is the expected payoff
        """
        self.advertiser_pay = advertiser_pay
        
        # estimate bid value
        self.data['bid_value'] = (advertiser_pay - self.data[bid_price_column]) * self.data[win_rate_column]
        self.data['advertiser_pay'] = advertiser_pay
        self.bid_value_data = self.data[['advertiser_pay', 'bid_price', 'bid_value']]
        return self.bid_value_data
    
    @property
    def compute_optimal_bid(self) -> float:
        """This is an attribute that returns the optimal bid price
        Returns:
            float: Bid price which maximizes revenue by choosing the highest expected payoff or bid value
        """
        optimal_bid_price = (self.bid_value_data[self.bid_value_data['bid_value'] == 
                                                 max(self.bid_value_data['bid_value'])]
                                                ['bid_price'].item()
                            )
        return optimal_bid_price
        
    
    ## function to plot bid value per bid price
    @property
    def plot_bid_value(self):
        """This is an attribute that returns a bar plot of expected payoff or bid value at various bid prices
        """
        self.bid_value_data.plot(kind='bar', x='bid_price', y='bid_value', 
                                 title=f'Estimated bid values for various bid price at ${self.advertiser_pay} (advertiser pay)'
                                )
    
    


