import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle";
import report from "./data/testReport.json";
import { Fragment, useEffect, useState } from "react";
import "./App.css";

function App() {
  const formatData = () => {
    const result = [];
    Object.values(report["API URL"]).forEach((e, i) => {
      const fmtData = {
        Scenario: report["Scenario"][i + 1],
        "API URL": e,
        Method: report["Method"][i + 1],
        "Request body": report["Request body"][i + 1],
        "Response time": report["Response time"][i + 1],
        Status: report["Status"][i + 1],
        "Actual result": report["Actual result"][i + 1],
        "Expected result": report["Expected result"][i + 1],
      };
      result.push(fmtData);
    });

    return result;
  };

  const [data, setData] = useState(formatData());

  useEffect(() => setData(formatData()), []);

  return (
    <div className="App container mt-5">
      <h1 className="mb-5">
        Reports
        <div className="btn-group ms-3">
          <button
            className="btn btn-secondary btn-sm dropdown-toggle"
            type="button"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            Filter status
          </button>
          <ul className="dropdown-menu">
            <li onClick={() => setData(formatData())}>
              <p className="dropdown-item">
                All
              </p>
            </li>
            <li
              onClick={() => setData(formatData().filter((v) => v["Status"]))}
            >
              <p className="dropdown-item">
                Passed
              </p>
            </li>
            <li
              onClick={() => setData(formatData().filter((v) => !v["Status"]))}
            >
              <p className="dropdown-item">
                Failed
              </p>
            </li>
          </ul>
        </div>
        <a
          href="/testReport.xlsx"
          className="ms-2 btn btn-light"
          role="button"
          download
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            className="bi bi-cloud-download"
            viewBox="0 0 16 16"
          >
            <path d="M4.406 1.342A5.53 5.53 0 0 1 8 0c2.69 0 4.923 2 5.166 4.579C14.758 4.804 16 6.137 16 7.773 16 9.569 14.502 11 12.687 11H10a.5.5 0 0 1 0-1h2.688C13.979 10 15 8.988 15 7.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 2.825 10.328 1 8 1a4.53 4.53 0 0 0-2.941 1.1c-.757.652-1.153 1.438-1.153 2.055v.448l-.445.049C2.064 4.805 1 5.952 1 7.318 1 8.785 2.23 10 3.781 10H6a.5.5 0 0 1 0 1H3.781C1.708 11 0 9.366 0 7.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383z" />
            <path d="M7.646 15.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 14.293V5.5a.5.5 0 0 0-1 0v8.793l-2.146-2.147a.5.5 0 0 0-.708.708l3 3z" />
          </svg>
        </a>
      </h1>
      {data.length !== 0 ? (
        <div className="accordion" id="accordionPanelsStayOpenExample">
          {data.map((val, index) => (
            <Fragment key={index}>
              <p className="m-0 mb-2">
                <span className="badge rounded-pill text-bg-secondary me-2">
                  Scenario #{index + 1}
                </span>
                {val["Scenario"]}
              </p>
              <div className="accordion-item mb-5">
                <h2
                  className="accordion-header"
                  id={"panelsStayOpen-heading" + index}
                >
                  <button
                    className="accordion-button d-flex justify-content-between"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target={"#panelsStayOpen-collapse" + index}
                    aria-expanded="true"
                    aria-controls={"panelsStayOpen-collapse" + index}
                  >
                    <div>
                      <p className="api_title_url">
                        <span className="badge p-2 px-3 rounded-pill text-bg-warning">
                          {val["Method"]}
                        </span>{" "}
                        {val["API URL"]}
                      </p>
                    </div>
                    <div>
                      {val["Status"] ? (
                        <span className="badge text-bg-success">Passed</span>
                      ) : (
                        <span className="badge text-bg-danger">Failed</span>
                      )}
                    </div>
                  </button>
                </h2>
                <div
                  id={"panelsStayOpen-collapse" + index}
                  className="accordion-collapse collapse show"
                  aria-labelledby={"panelsStayOpen-heading" + index}
                >
                  <div className="accordion-body">
                    <div className="row">
                      <p>
                        <span className="badge rounded-pill text-bg-secondary">
                          Response time
                        </span>{" "}
                        {val["Response time"] + " seconds"}
                      </p>
                    </div>
                    <div className="row">
                      <div className="col-6">
                        <p>
                          <span className="badge rounded-pill text-bg-primary">
                            Actual result
                          </span>
                        </p>
                        <pre style={{ height: "25rem" }}>
                          <p style={{ overflowWrap: "break-word" }}>
                            {JSON.stringify(val["Actual result"], null, "\t")}
                          </p>
                        </pre>
                      </div>

                      <div className="col-6">
                        <p>
                          <span className="badge rounded-pill text-bg-primary">
                            Expected JSON Schema
                          </span>
                        </p>
                        <pre style={{ height: "25rem" }}>
                          <p style={{ overflowWrap: "break-word" }}>
                            {JSON.stringify(
                              JSON.parse(val["Expected result"]),
                              null,
                              "\t"
                            )}
                          </p>
                        </pre>
                      </div>
                    </div>
                    <div className="row">
                      {val["Method"] === "POST" && (
                        <>
                          <p>
                            <span className="badge rounded-pill text-bg-primary">
                              Example request body
                            </span>
                          </p>
                          <pre style={{ height: "20rem" }}>
                            <div className="col-12">
                              {JSON.stringify(
                                JSON.parse(val["Request body"]),
                                null,
                                "\t"
                              )}
                            </div>
                          </pre>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </Fragment>
          ))}
        </div>
      ) : (
        <>
          <p>Result: 0</p>
        </>
      )}
    </div>
  );
}

export default App;
