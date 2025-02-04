export const NavBar = () => {
  return(
    <div
      style={{
        backgroundColor: '#303641',
        height: 40
      }}
    >
      <span className="logo" href="#"
          style={{float: 'left'}}
      >
          ReviewerAPP
      </span>

      {/*<Select 
          defaultValue={0}
          size="small"
          options={[
              {value: 0, label: "Case 1"},
              {value: 1, label: "Case 2"},
              {value: 2, label: "Case 3", disabled: false,}
          ]}
          onChange={e=>setSelectedCase(e)}
          style={{
              width: 200,
              float: 'left',
              marginTop: 10
          }}
      />*/}

      <span
          style={{
              float: 'left', color: "white", lineHeight: 3,
              marginLeft: 20
          }}
      >
          <b>Case Title: </b>
      </span>

    </div>
  );
}