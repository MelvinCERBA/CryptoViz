# Data

## Introduction

Our solution aims to help people looking to make money with cryptocurrencies. Here are the ways people generate income in the crypto environnement:
- **Trading:** Buying low and selling high.
    - *Fiat/Crypto*
    - *Spot* : trading crypto/crypto
    - *Futures* : ?
- **Holding:** Long-term investment in anticipation of price appreciation.
- **Mining:** Verifying transactions and earning block rewards.
- **Staking:** Participating in PoS consensus to earn transaction fees or new coins.
- **Initial Coin Offerings (ICOs) or Token Sales:** Investing in new projects.
- **Yield Farming and Liquidity Provision:** Providing liquidity to earn fees or tokens.

For this project, let's focus on Trading and Holding. These boil down to the question **How is the value of the different cryptocurrencies going to evolve ?** To answer this question, we shall try to provide a muli-layered analysis :

1. **Technical Analysis:** Study price charts, create indicators and use predictive models.
    - Purely based on price data
    - Use of 
        - *Chart patterns*
        - *Indicators (Moving averages, Bolling bands, Relative strength index, ...)*
        - Volume analysis (Examine trade volumes as an indication of momentum or trend reversals)
2. **Fundamental Analysis:** Evaluate the intrinsic value of a cryptocurrency.
    - *Whitepapers:* Analyze the project's whitepaper for its vision, use-case, and technology.
    - *Tokenomics:* Study the token distribution, utility, and supply metrics.
    - *Regulation:* Assess the impact of new/incoming regulations on the prooject. 
    - *Team and Partnerships:* Evaluate the credibility and track record of the team and any strategic partnerships.
    - *Market Position:* Assess market demand, competition, and the asset's potential for adoption.
3. **Sentiment Analysis:** Gauge market sentiment through news and social media.
    - Assess sentiment towards the project on social media, news sites, and forums.
        - use NLP to detect sentiment
        - Create scores/indicators : ponderate the results (numbers, strength of opinions, site reliability, ... )
            - idea: the user chooses/rates the media they trust

We will have 2 types of customuers :
1. Those willing to sell:
    - Looking to sell for the best price
    - Should I sell now, or will the price keep going up ?
    - Should I sell now to minimize my loss, or will the value rebound ?
2. Those looking for opportunities to invest in:
    - What are low valued currencies that will grow ? --  analysis
    - Safe investments ? --  analysis
    - Opportunities related to new projects ? -- news feed + analysis

## Our data

### Data to present (Web App)

1. **Technical Analysis:** Historical data, Analytics & Predictions for :
    - *prices* of currencies on different exchanges
    - *volumes* of currency on different exchanges
2. **Fundamental Analysis:** Evaluate the intrinsic value of a cryptocurrency.
    - Currency's' *Whitepapers* 
    - *Tokenomics Recap:* 
        - Token supply (histoical data, analytics, predictions)
        - Liquidity (histoical data, analytics, predictions) 
    - *Regulation:* 
        - legal news feed related to the currency 
    - *Market Position:* Assess market demand, competition, and the asset's potential for adoption.
        - community engagement ~ sentiment
        - market share
        - on-chain activity 
            - Websites like Etherscan for Ethereum or Blockchair for multiple blockchains can provide real-time data on transactions, accounts, blocks, and more.
            - Platforms like Nansen, Glassnode, or Coin Metrics offer advanced analytics, including token flows, ownership distribution, and other critical metrics.
            - APIs: Most blockchains offer APIs that allow you to directly query the blockchain for specific data points.
            - Node Operations: Running a full or partial node will give you direct access to raw blockchain data. This option requires substantial technical expertise and computational resources.
            - metrics to monitor:
                - Transaction Volume: Tracks the total value being transferred over the network, often correlated with asset demand.
                - Active Addresses: 
                - Hash Rate: For Proof-of-Work blockchains 
                - Gas Fees: 
                - Flows
                - Smart Contract Interaction
3. **Sentiment Analysis:** media related to cryptocurrency
    - news feeds
    - social media posts

One idea would be to create indicators and adjust them until we can get an AI model 

### Data to compute (Spark App)