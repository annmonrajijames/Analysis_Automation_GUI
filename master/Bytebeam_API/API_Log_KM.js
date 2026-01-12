const axios = require('axios');
const XLSX = require('xlsx');

// Define the request configuration for the first API call (C2C GPS Data)
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

// Define the request configuration for the second API call (CAN Parsed Joined Data)
const can_parsed_joined_panel_data_req = {
  method: "POST",
  url: "https://cloud.bytebeam.io/api/v1/panel-data",
  headers: {
    "x-bytebeam-tenant": "lectrix",
    "content-type": "application/json",
    "x-bytebeam-api-key": "82e9b8c1-98ab-4128-bfcf-2ae9e0cbe323"
  },
  data: JSON.stringify({
    startTime: 1721714472168,
    endTime: 1724392872168,
    filterBys: {id: ["9"]},
    groupBys: [],
    panels: [{
      type: "timeseries_table",
      table: "can_parsed_joined",
      columns: [
        // List of columns (omitted for brevity)
        "CellUnderVolWarn_9",
        "percentage_of_can_ids",
        "Dchg_Accumulative_Ah_14",
        "CellOverVolProt_9",
        "ChargerType_12",
        "CellVol02_1",
        "AC_Current_340920579",
        "PcbTemp_12",
        "Reverse_Pulse_408094978",
        "MotorSpeed_340920578",
        "LatchProtection_12",
        "Temp6_10",
        "Temp3_10",
        "ForwardParking_Mode_Ack_408094978",
        "FetFailure_9",
        "CellOverDevProt_9",
        "AvgCellVol_5",
        "MinVoltId_5",
        "DriveStatus1_Ride_418513673",
        "LoadDetection_12",
        "Set_Regen_418513673",
        "number_of_records",
        "Overcurrent_Fault_408094978",
        "BatteryVoltage_340920578",
        "ChgOverCurrProt_9",
        "BuzzerStatus_12",
        "MinCellVol_5",
        "Throttle_Error_408094978",
        "CellVol04_1",
        "CellOverVolWarn_9",
        "CellVol08_2",
        "CellBalFeatureStatus_12",
        "Temp2_10",
        "CellUnderVolProt_9",
        "Temp8_10",
        "Throttle_408094978",
        "Hill_hold_Ack_408094978",
        "DchgUnderTempProt_9",
        "CellVol06_2",
        "AfeTemp_12",
        "LatchType_12",
        "DI1_12",
        "Wakeup_Ack_408094978",
        "IgnitionStatus_12",
        "PreChgFetStatus_9",
        "DchgOverTempWarn_9",
        "MCU_ID_408094979",
        "BMS_Serial_No_MUX_11",
        "Temp1_10",
        "DriveStatus2_Reverse_Request_418513673",
        "Mode_Ack_408094978",
        "ModeR_Pulse_408094978",
        "VCU_ID_418513673",
        "ResSocProt_9",
        "CellVol12_3",
        "HwVer_13",
        "DchgFetStatus_9",
        "Temp4_10",
        "ChgPeakProt_9",
        "Side_Stand_Ack_408094978",
        "DchgUnderTempWarn_9",
        "ChgFetStatus_9",
        "ImmoChg_12",
        "timestamp",
        "ChargeSOP_16",
        "PackVol_6",
        "BMS_Serial_No__1_7_11",
        "FWSubVer_13",
        "CellVol05_2",
        "ShortCktProt_9",
        "DO2_12",
        "BattLowSocWarn_9",
        "ChgUnderTempWarn_9",
        "PackCurr_6",
        "BmsStatus_8",
        "ChgOverTempProt_9",
        "InternalFWSubVer_21",
        "Chg_Accumulative_Ah_14",
        "Park_Pulse_408094978",
        "CellVol16_4",
        "PackUnderVolProt_9",
        "CellVol07_2",
        "InternalFWVer_21",
        "sequence",
        "CellVol01_1",
        "LedStatus_9",
        "MaxTempId_7",
        "CellVol15_4",
        "CellVol09_3",
        "DschgPeakProt_9",
        "Controller_Over_Temeprature_408094978",
        "Motor_Temperature_408094979",
        "_3v3Vol_15",
        "ChargerDetection_12",
        "Actual_SoC_18",
        "SOCAh_8",
        "SOC_8",
        "Controller_Undervoltage_408094978",
        "Usable_Capacity_Ah_18",
        "BMS_Serial_No_Bytes_8_14_11",
        "Mode_Request_418513673",
        "PackOverVolWarn_9",
        "Temp7_10",
        "ChgOverTempWarn_9",
        "DchgOverTempProt_9",
        "SOH_8",
        "Temp5_10",
        "DchgOverCurrProt_9",
        "BatteryCurrent_340920578",
        "MaxCellVol_5",
        "Direction_Ack_408094978",
        "DC_Current_Limit_418513673",
        "Ride_Ack_408094978",
        "MaxVoltId_5",
        "BMS_Serial_No__15_11",
        "_12vVol_15",
        "MCU_Fault_Code_408094979",
        "CycleCount_7",
        "MCU_Temperature_408094979",
        "TempSenseFault_9",
        "Hill_Hold_418513673",
        "MinTemp_7",
        "CellVol13_4",
        "DchgSOP_16",
        "Drive_418513673",
        "DriveError_Motor_hall_408094978",
        "Motor_Stalling_408094978",
        "CellVol14_4",
        "FetTemp_8",
        "WakeUp_Request_418513673",
        "PackUnderVolWarn_9",
        "AC_Voltage_340920580",
        "MOSFET_Protection_408094978",
        "CellVol10_3",
        "Motor_Over_Temeprature_408094978",
        "ConfigVer_21",
        "FetTempProt_9",
        "number_of_can_ids",
        "ChgAuth_9",
        "Brake_Pulse_408094978",
        "CellVol03_1",
        "ForwardPark_Request_418513673",
        "CanCommDetection_12",
        "DriveStatus_Regenerative_Braking_408094978",
        "MinTempId_7",
        "ResStatus_9",
        "ModeL_Pulse_408094978",
        "CellVolMinMaxDev_7",
        "DriveError_Controller_OverVoltag_408094978",
        "ImmoDchg_12",
        "CellChemType_12",
        "ChgUnderTempProt_9",
        "CellVol11_3",
        "MaxTemp_7",
        "RefVol_15",
        "PackOverVolProt_9",
        "_5vVol_15",
        "DO1_12",
        "SideStand_Pulse_408094978",
        "FwVer_13",
        "Motor_Phase_loss_408094978",
        "DI2_12",
        "ActiveCellBalStatus_9",
      ],
      sortOrder: "desc",
      rowsPerPage: 1000,
      page: 1
    }]
  })
};

// Function to fetch data from API and export to Excel
async function fetchAndExportData() {
  try {
    // Fetch and export C2C GPS Data
    const gpsResponse = await axios(c2c_gps_panel_data_req);
    const gpsData = gpsResponse.data;
    if (!gpsData || !gpsData[0] || !gpsData[0].data || !gpsData[0].data.data) {
      throw new Error("Unexpected C2C GPS API response structure");
    }
    const gpsRows = gpsData[0].data.data;
    const gpsWorksheet = XLSX.utils.json_to_sheet(gpsRows);
    const gpsWorkbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(gpsWorkbook, gpsWorksheet, "C2C_GPS_Data");
    XLSX.writeFile(gpsWorkbook, "km.xlsx");
    console.log("C2C GPS Data exported to km.xlsx");

    // Fetch and export CAN Parsed Joined Data
    const canResponse = await axios(can_parsed_joined_panel_data_req);
    const canData = canResponse.data;
    if (!canData || !canData[0] || !canData[0].data || !canData[0].data.data) {
      throw new Error("Unexpected CAN Parsed Joined API response structure");
    }
    const canRows = canData[0].data.data;
    const canWorksheet = XLSX.utils.json_to_sheet(canRows);
    const canWorkbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(canWorkbook, canWorksheet, "can_parsed_joined_Data");
    XLSX.writeFile(canWorkbook, "log.xlsx");
    console.log("CAN Parsed Joined Data exported to log.xlsx");

  } catch (error) {
    console.error("Error fetching data: ", error);
  }
}

// Call the function to fetch data and export to Excel
fetchAndExportData();
