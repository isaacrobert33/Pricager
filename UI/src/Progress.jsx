import React from "react";
import { CircularProgress} from '@chakra-ui/react';

const Progress = () => {
    return (
        <div className="spinner-container">
            <CircularProgress size={"80px"} thickness={"4px"} isIndeterminate css={{marginTop: "15%"}}/>
        </div>
    )
};

export default Progress;