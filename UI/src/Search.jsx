import React, { useEffect } from "react";
import { useState } from "react";
import axios from "axios";
import search from "./search.svg";
import amazon from "./amazon.svg";

const HOST = "http://robertix.pythonanywhere.com";

const ProductCard = ({ id, title, price, site, img, link="#", badge=null }) => {
    if (title.split(" ").length > 10) {
      title = title.split(" ").slice(0, 11).join(" ");
    }
    return (
        <div key={id} className="product-card">
          {
            badge ? (<span className="badge">{badge}</span>): (<></>)
          }
          <img width={"78px"} height={"78px"} src={img} alt={title}></img>
          <div className="product-details">
            <h4><a href={link}>{title}</a></h4>
            <p>{price}</p>
            <p>Price for: <b>{site}</b></p>
          </div>
        </div>
    )
}
const Search = () => {
    // const [query, setQuery] = useState(undefined);
    const [one, setOne] = useState([]);
    const [two, setTwo] = useState([]);
    const [three, setThree] = useState([]);
    const [highestProduct, setHighest] = useState(undefined);
    const [cheapestProduct, setCheapest] = useState(undefined);
    const [dynamicHighest, setDynamicHighest] = useState({});
    const [dynamicCheapest, setDynamicCheapest]= useState({});
    const [resultTabs, setResultTabs] = useState([]);
    const [page, setPage] = useState(1);
    const [activeTab, setActive] = useState("");
    const [order, setOrder] = useState("desc");

    useEffect((e) => {
      document.getElementById("search-tab").style.textDecoration = "underline";
      document.getElementById("products-tab").style.textDecoration = "none";
    })

    async function fetchResult(pageNo=null, order_=null) {
        console.log(pageNo)
        let pageVal = page;
        let orderVal = order;
        if (pageNo) {
          pageVal = pageNo;
        } 
        if (order_) {
          orderVal = order_;
        }
        let query = document.getElementById("search-q").value;
        let {data} = await axios.get(`${HOST}/search?q=${query}&limit=${30}&page=${pageVal}&order=${orderVal}`);
        data = data.data;
        setResultTabs(Object.keys(data.products));
        setOne(data.products.amazon);
        setTwo(data.products.bulkreef);
        setThree(data.products.saltwateraquarium);
        setHighest(data.product_metric.highest);
        setCheapest(data.product_metric.cheapest);
        setDynamicHighest(data.dynamic_metric.highest);
        setDynamicCheapest(data.dynamic_metric.cheapest);
        
    }

    const sortResult = () => {
      setOrder(order === "desc" ? "asc" : "desc");
      fetchResult(page, order);
    }

    const switchTab = (tab_name) => {
      let i;
      for (i=0; i<document.getElementsByClassName("tab").length; i++) {
        console.log(resultTabs[i]);
        document.getElementsByClassName("tab")[i].style.display = "none";
        document.getElementById(`${resultTabs[i]}-btn`).style.color = "#002e25";
        document.getElementById(`${resultTabs[i]}-btn`).style.backgroundColor = "azure";
      }
      document.getElementById(tab_name).style.display = "flex";
      document.getElementById(`${tab_name}-btn`).style.color = "azure";
      document.getElementById(`${tab_name}-btn`).style.backgroundColor = "#002e25";
      setActive(tab_name.charAt(0).toUpperCase() + tab_name.slice(1));
    }

    var timeID;
    const inputQ = () => {
        clearTimeout(timeID);
        timeID = setTimeout(fetchResult, 1000)
    }

    const previous = () => {
      console.log(page);
      if (page > 1) {
        setPage(page - 1);
      }
      fetchResult(page - 1);
    }
    const next = () => {
      setPage(page + 1);
      fetchResult(page + 1);
    }
    return (
      <div className='search'>
        <img src={search} alt={"search"}></img>
        <br></br>
        <div>
        <input onChange={inputQ} className="search-bar" id="search-q"  placeholder="Which product prices do you need?"></input>
        </div>
        <div className="search-tabs">
          {
            resultTabs.map(
              (tab_name) => (
                <span id={`${tab_name}-btn`} onClick={()=> (switchTab(tab_name))} key={tab_name}>{tab_name.charAt(0).toUpperCase() + tab_name.slice(1)}</span>
              )
            )
          }
          
        </div>
          {
            resultTabs.length > 0 ? (<span onClick={(e) => (sortResult())} id="sort"></span>) : (<></>)
          }
        
          {
            highestProduct ? (
              <div className="special-tab">
                <ProductCard key={highestProduct.product_preview} title={highestProduct.product_title} price={highestProduct.product_price} img={highestProduct.product_preview} badge={"Highest Price"} site={highestProduct.store}/>
                <ProductCard key={cheapestProduct.product_preview} title={cheapestProduct.product_title} price={cheapestProduct.product_price} img={cheapestProduct.product_preview} badge={"Cheapest Price"} site={cheapestProduct.store}/>
                <ProductCard key={dynamicHighest.product_preview} title={dynamicHighest.product_title} price={dynamicHighest.product_price} img={dynamicHighest.product_preview} badge={"Highest Price"} site={"Dynamic"}/>
                <ProductCard key={dynamicCheapest.product_preview} title={dynamicCheapest.product_title} price={dynamicCheapest.product_price} img={dynamicCheapest.product_preview} badge={"Cheapest Price"} site={"Dynamic"}/>
              </div>
            ) : (
              <></>
            )
          }
        
        <div className="search-results">
          {
            resultTabs?.length > 0 ? (
              <>
                <div className={"tab"} id={"amazon"}>
                  <h2>Result for: "{activeTab}"</h2>
                  {
                    one?.length > 0 ? (
                      one.map(
                        (data) => (
                          <ProductCard key={one.indexOf(data)} id={one.indexOf(data)} title={data.product_title} price={data.product_price} site={"Amazon"} img={amazon} link={`https://www.amazon.com${data.product_url}`}/>
                        )
                      )
                    ) : (
                      <i>No Product here!</i>
                    )
                  }
                </div>
                <div className={"tab"} id={"bulkreef"}>
                  <h2>Result for: "{activeTab}"</h2>
                  {
                    two?.length > 0 ? (
                      two.map(
                        (data) => (
                          <ProductCard key={two.indexOf(data)} id={two.indexOf(data)} title={data.product_title} price={data.product_price} site={"Bulkreef"} img={data.product_preview} />
                        )
                      )
                    ) : (
                      <i>No Product here!</i>
                    )
                  }
                </div>
                <div className={"tab"} id={"saltwateraquarium"}>
                  <h2>Result for: "{activeTab}"</h2>
                  {
                    three?.length > 0 ? (
                      three.map(
                        (data) => (
                          <ProductCard key={three.indexOf(data)} id={three.indexOf(data)} title={data.product_title} price={data.product_price} site={"Salt Water Aquarium"} img={data.product_preview} />
                        )
                      )
                    ) : (
                      <i>No Product here!</i>
                    )
                  }
                </div>
              
              {
                resultTabs?.length > 0 ? (
                  <div className="pagination">
                    <b onClick={previous}>{"<"}</b>
                    <b>{page}</b>
                    <b onClick={next}>{">"}</b>
                </div>
                ) : (
                  <></>
                )
              }
            </>
            ) : (
              <></>
            )
            
          }
        </div>
      </div>
    )
}

export default Search;
