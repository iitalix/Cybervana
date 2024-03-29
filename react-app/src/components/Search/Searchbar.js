import React, {useState, useRef, useEffect} from "react";
import {FaSearch} from "react-icons/fa";
import ResultsList from "../../components/Search/ResultsList";

const SearchBar = ({setResults, setIsResultsOpen, results, isResultsOpen}) => {
  const [search, setSearch] = useState("");
  const resultsContainerRef = useRef(null);

  const fetchData = (value) => {
    fetch("/api/vehicles/all")
      .then((response) => response.json())
      .then((json) => {
        const filteredResults = json.filter((vehicle) => {
          return (
            vehicle &&
            (
              vehicle.model.toLowerCase().includes(value) ||
              vehicle.make.toLowerCase().includes(value)
            )
          );
        });
        setResults(filteredResults);
        setIsResultsOpen(true);
      });
  };

  const handleChange = (value) => {
    setSearch(value);
    fetchData(value);

  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      setSearch("");
    };

    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);

  const clearSearch = () => {
    setResults([]);
    setIsResultsOpen(false);
  };

  const handleOutsideClick = (event) => {
    if (
      resultsContainerRef.current &&
      !resultsContainerRef.current.contains(event.target)
    ) {
      clearSearch();
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleOutsideClick);

    return () => {
      document.removeEventListener("click", handleOutsideClick);
    };
  }, []);

  return (
<div className="input-wrapper">
      <FaSearch id="search-icon" />
      <input
        className="search-input"
        placeholder="Search All Vehicles..."
        value={search}
        onChange={(e) => handleChange(e.target.value)}
      />
      <div className="results-container" ref={resultsContainerRef}>
        {isResultsOpen && search !== "" && ( // Add this condition
          <ResultsList results={results} clearSearch={clearSearch} />
        )}
      </div>
    </div>
  );
};

export default SearchBar;
