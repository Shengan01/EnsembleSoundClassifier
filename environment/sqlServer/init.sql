-- Create the Instrument table
CREATE TABLE Instruments (
    instrumentID SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    audioCount INT
);

-- Create the AudioFiles table
CREATE TABLE AudioFiles (
    audioID SERIAL PRIMARY KEY,
    filePath VARCHAR(100) NOT NULL,
    sampleRate INT,
    duration INT,
    instrumentID INT,
    FOREIGN KEY (instrumentID) REFERENCES Instruments(instrumentID)
);

-- Create the Processed table
CREATE TABLE Processed (
    processedID SERIAL PRIMARY KEY,
    instrumentID INT,
    audioID INT,
    fixedLength INT,
    spectrogramPath VARCHAR(100),
    mfccPath VARCHAR(100),
    augmentation VARCHAR(50) CHECK (augmentation IN ('original', 'time_stretch', 'pitch_shifting', 'noise' )),
    FOREIGN KEY (instrumentID) REFERENCES Instruments(instrumentID),
    FOREIGN KEY (audioID) REFERENCES AudioFiles(audioID)
);