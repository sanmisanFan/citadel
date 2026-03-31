export const NavBar = () => {
    return (
        <div
            style={{
                backgroundColor: '#303641',
                height: 40
            }}
        >
            <span className="logo" href="#"
                style={{ float: 'left' }}
            >
                ReviewerAPP
            </span>

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
