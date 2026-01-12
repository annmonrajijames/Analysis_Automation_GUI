const axios = require('axios');
const fs = require('fs');
const XLSX = require('xlsx');

// Define the API request
const c2c_gps_panel_data_req = {
  method: "POST",
  url: "https://cloud.bytebeam.io/api/v1/panel-data",
  headers: {
    "content-type": "application/json",
    "x-bytebeam-tenant": "lectrix",
    "x-bytebeam-api-key": "82e9b8c1-98ab-4128-bfcf-2ae9e0cbe323" // Replace with your API key
  },
  data: JSON.stringify({
    startTime: 1721714472168,
    endTime: 1724392872168,
    filterBys: {
      id: ["9"],
    },
    groupBys: [],
    panels: [
      {
        type: "timeseries_table",
        table: "c2c_gps",
        columns: [
          "geoid_height",
          "course_over_ground",
          "pdop",
          "vdop",
          "gps_date",
          "satellites_used",
          "fix_type",
          "ground_speed_kmph",
          "longitude",
          "satellites_in_view",
          "timestamp",
          "altitude",
          "latitude",
          "sequence",
          "gps_time",
          "hdop",
        ],
        sortOrder: "desc",
        rowsPerPage: 100,
        page: 1,
      },
    ],
  }),
};

// Function to fetch data from API and export to Excel
async function fetchAndExportData() {
  try {
    // Make the API request
    const response = await axios(c2c_gps_panel_data_req);

    // Log the entire response to inspect its structure
    console.log("API Response: ", response.data);

    const data = response.data;

    // Ensure the response contains the expected data
    if (!data || !data[0] || !data[0].data || !data[0].data.data) {
      throw new Error("Unexpected API response structure");
    }
    
    // Extract relevant data for the Excel file
    const rows = data[0].data.data; // Adjusted to access the nested data array

    // Prepare the data for Excel
    const worksheet = XLSX.utils.json_to_sheet(rows);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "C2C_GPS_Data");

    // Write to Excel file
    XLSX.writeFile(workbook, "gps_data.xlsx");
    console.log("Data exported to gps_data.xlsx");

  } catch (error) {
    console.error("Error fetching data: ", error);
  }
}

// Call the function to fetch data and export to Excel
fetchAndExportData();
