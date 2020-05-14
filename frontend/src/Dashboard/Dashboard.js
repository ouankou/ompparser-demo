import React from 'react';
import {Button, Select, Upload} from 'antd';
import 'antd/dist/antd.css';
import './Dashboard.css';
import { ToolOutlined, UploadOutlined, RotateRightOutlined, SaveOutlined, HomeOutlined} from '@ant-design/icons';
import axios from 'axios';
import Img from 'react-image';

const Option = Select.Option;

const children = [];

children.push(<Option key="1">COMPILER:GCC8.0</Option>);
children.push(<Option key="2">COMPILER:GCC7.0</Option>);
children.push(<Option key="3">COMPILER:GCC6.0</Option>);
children.push(<Option key="4">COMPILER:GCC5.0</Option>);
children.push(<Option key="5">RUNTIME:LLVM</Option>);
children.push(<Option key="6">RUNTIME:GOMP</Option>);
children.push(<Option key="7">LIB:MPI</Option>);
children.push(<Option key="8">LIB:MKL</Option>);
              
class Dashboard extends React.Component {
    state = {
        myDisplay: 'row',
        myWidth: 0,
        myFile: null,
        myPreview: null,
        myCompiler: 'GCC8',
        myRuntime: 'LLVM',
        myLib: null,
        myKey: "myKey",
        myStatus: null,
        myOutput: null,
        myRes: null
    };
    
    constructor(props) {
        super(props);
        this.resize.bind(this);
    };

    componentDidMount() {
        this.screenChange();

        if (document.body.clientWidth <= 700) {
            this.setState({myDisplay: 'column'});
        } else {
            this.setState({myDisplay: 'row'});
        }
              
        this.setState({myPreview: null});
    };

    componentWillUnmount() {
        window.removeEventListener('resize',this.resize);
    };
    
    resize  = () => {
        this.setState({myWidth: document.body.clientWidth});
        console.log(this.state.myWidth);
        if (this.state.myWidth <= 700) {
            this.setState({myDisplay: 'column'});
        } else {
            this.setState({myDisplay: 'row'});
        }
    };

    screenChange = () => {
        window.addEventListener('resize', this.resize);
    }

/*
 
 The desired function call could be like:
 
 def func():
    return { "status":"...", "msg": "..." }
 
 status could be SUCCESS or FAILED; msg could be the url of AST or error message
 
 In the demo for now, I have:
 
 {
   "msg": "...",
   "status": "..."
 }

Of course, CORS is needed

 */
    Onchg = (info) => {
        this.setState({myFile: info.file.name});
        this.setState({myKey: info.file.response});
        
        const tmp = new FileReader();
        
        tmp.readAsText(info.file.originFileObj); // This is only part of Blob!
        tmp.onload = (res) => {
              this.setState({myPreview: res.target.result});
        }

        console.log(info);

        let myStr = "/tmp/" + this.state.myKey + "/" + this.state.myFile + ".pragmas";
        this.setState({myOutput: myStr});
        
        console.log(this.state);
    };

    Cpl = () => {
        console.log(this.state.myOutput);
        axios.get("/task?content=" + "pragmas" + "&tid=" + this.state.myKey + "&fn=" + this.state.myFile).then(res=>{this.setState({myRes: res.data}); console.log(res.data)});

        if (this.state.myOutput != null) this.setState({myStatus: "SUCCESS"});
    };

    Onclk = () => {
       if (this.state.myDisplay === 'row') {
           this.setState({myDisplay: 'column'});
       } else {
           this.setState({myDisplay: 'row'});
       }

       console.log('display changed!');
    };

    render() {
        let OUTPUT;

        if (this.state.myStatus === "SUCCESS") {
              OUTPUT = <textarea className = "outputbox" value = {this.state.myRes}/>
        } else {
              OUTPUT = <textarea className = "outputbox" placeholder="Results/Error messages will be shown here"/>
        }

        let myAction = "/task"

        return (
            <div>
                <div className = "logo">
                    <b><ToolOutlined /> | ompparser online demo</b>
                </div>
                <div className = "opts">
                    <Button><HomeOutlined /></Button>
                    <Upload action = {myAction} onChange = {(info) => this.Onchg(info)} showUploadList = {false} ><Button><UploadOutlined /></Button></Upload>
                    <Button><SaveOutlined /></Button>
                    <Button onClick = {() => this.Onclk()}><RotateRightOutlined /></Button>
                    <Button type="primary" onClick = {() => this.Cpl()}>Analyze</Button>
                </div>
                <div className = "tags">
                    <Select
                      mode="multiple"
                      style={{ width: '100%' }}
                      placeholder="Please select compile configurations"
                      defaultValue={['1', '5']}
                    >
                      {children}
                    </Select>
                </div>
                <div className = "texts" style = {{flexDirection: this.state.myDisplay}}>
                    <textarea className = "inputbox" placeholder="Type or upload your code" value = {this.state.myPreview}/>
                    { OUTPUT }
                </div>
            </div>
        )
    };
}

export default Dashboard;
