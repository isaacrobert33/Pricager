import axios from "axios";
import React, { useEffect } from "react";
import Progress from "./Progress";
import { useState } from "react";

// var productFetched = false;
const HOST = "https://robertix.pythonanywhere.com";

const ProductRow = ({id, title, price, img, ranges=[]}) => {
  
  return (
    <div key={id} className="product-row">
      <span className="product-badge">{"Dynamic"}</span>
      <div className="product-preview">
        <img width={"128px"} height={"128px"} src={img} alt={price}></img>
      </div>
      <div className="product-info">
        <h2>{title}</h2>
        <span>{price}</span>
       
        <p style={{fontWeight: "bold", fontSize: "12px"}}>Price Ranges:</p>
        {
          ranges.map(
            (data) => (
              <span className="price-range" key={data.store}><b>{data.store}:</b> <span style={{color: "#298798"}}>{data.cheapest.product_price}</span> - <span style={{color: "#be4b2e"}}>{data.highest.product_price}</span></span>
            )
          )
        }
      </div>
    </div>
  )
}

const DynamicProducts = () => {
    const [products, setProducts] = useState([]);
    const [page, setPage] = useState(1);
    const [isLoading, setLoading] = useState(false);

    const fetchProducts = async (pageNo = null) => {
      setLoading(true);
      let pageVal = page;
      if (pageNo) {
        pageVal = pageNo;
      }

      await axios.get(`${HOST}/dynamic?limit=${30}&page=${pageVal}`)
        .then(
          response => {
            setProducts(response.data.data);
            setLoading(false);
          }
        )
        .catch(
          err => {
            alert("Error fetching products, please check your connection!");
          }
        )
    }

    const previous = () => {
      if (page > 1) {
        setPage(page - 1);
      }
      fetchProducts(page - 1);
      window.scrollTo(0, 0);
    }
    const next = () => {
      setPage(page + 1);
      fetchProducts(page + 1);
      window.scrollTo(0, 0);
    }
    
    useEffect((e) => {
      document.getElementById("search-tab").style.textDecoration = "none";
      document.getElementById("products-tab").style.textDecoration = "underline";

      if (products.length<1) {
        fetchProducts(page);
      }
      
    })
    return (
      <div className='products'>
        {
          isLoading ? (
            <Progress></Progress>
          ) : (<></>)
        }
        {
          products?.length > 0 ? (
            <div className="products-list">
              {
                products.map(
                  (data) => (
                    <ProductRow key={`product-${products.indexOf(data)}`} id={`product-${products.indexOf(data)}`} title={data.title} price={data.price} img={data.preview} ranges={data.product_data.ranges} />
                  )
                )
              }
            </div>
          ) : (
            <i>No products from Dynamic</i>
          )
        }
        {
          products?.length > 0 ? (
            <div className="pagination">
              <b onClick={previous}>{"<"}</b>
              <b>{page}</b>
              <b onClick={next}>{">"}</b>
          </div>
          ) : (
            <></>
          )
        }
      </div>
    )
  }

export default DynamicProducts;